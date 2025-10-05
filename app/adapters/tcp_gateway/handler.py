import asyncio
import msgpack
import crcmod
from  app.core.logger import logger

MAGIC = b"\xab\xcd"

_crc8_func = crcmod.mkCrcFun(0x131, initCrc=0x00, xorOut=0x00)

def crc8(data: bytes) -> int:
    return _crc8_func(data)

async def _unpack_msgpack(data: bytes):
    try:
        return msgpack.unpackb(data, raw=False)
    except Exception as e:
        logger.warning(f"msgpack解包失败: {e} 原始data={data.hex()}")
        return None

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    buf = b""
    while True:
        try:
            chunk = await reader.read(1024)
            if not chunk:
                break
            buf += chunk

            while len(buf) >= 4:
                if buf[:2] != MAGIC:
                    idx = buf.find(MAGIC)
                    if idx == -1:
                        logger.info(f"丢弃无效数据: {buf[:16].hex()}")
                        buf = b""
                        break
                    logger.info(f"跳过至Magic头: {buf[:idx].hex()}")
                    buf = buf[idx:]
                    if len(buf) < 4:
                        break

                length = buf[2]
                crc_val = buf[3]

                if not (1 <= length <= 256):
                    logger.info(f"非法长度字段: {length}, 包头: {buf[:16].hex()}")
                    buf = buf[4:]
                    continue

                if len(buf) < 4 + length:
                    break

                data = buf[4 : 4 + length]
                if crc8(data) != crc_val:
                    logger.info(f"CRC校验失败: recv={crc_val}, calc={crc8(data)}, data={data.hex()}")
                    buf = buf[4 + length :]
                    continue

                payload = await _unpack_msgpack(data)
                if not payload:
                    buf = buf[4 + length :]
                    continue

                sn = payload.get("sn")
                if not sn:
                    logger.info(f"缺失sn字段: {payload}")
                    buf = buf[4 + length :]
                    continue

                # 事件管道对接：直接通过 event_bus 发布原始payload
                from  app.core.event_bus import event_bus
                await event_bus.publish("tcp_data_received", payload)
                logger.info(f"已推送事件: sn={sn}, payload={payload}")

                buf = buf[4 + length :]

        except Exception as e:
            logger.error(f"TCP处理异常: {e}")
            break
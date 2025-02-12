import logging
from typing import Optional


class GameLogger:
    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        if cls._instance is None:
            cls._instance = logging.getLogger('game')
            cls._instance.setLevel(logging.INFO)

            # 添加控制台处理器
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            cls._instance.addHandler(handler)

        return cls._instance 
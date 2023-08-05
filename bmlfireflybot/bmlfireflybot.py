import ast
from configparser import ConfigParser
from functools import wraps
from typing import Optional, List, Union, BinaryIO

from pyrogram import Client, types
from pyrogram.raw.all import layer
from pyrogram.types import Message, CallbackQuery


class BmlFireflyBot(Client):
    def __init__(self, version='0.0.0'):
        self.version = version
        self.name = name = self.__class__.__name__.lower()

        self.config = config = ConfigParser()
        config.read('config.ini')

        super().__init__(
            name,
            api_id=config.get('pyrogram', 'api_id'),
            api_hash=config.get('pyrogram', 'api_hash'),
            bot_token=config.get('pyrogram', 'bot_token'),
            workers=16,
            plugins=dict(root='bmlfireflybot/plugins'),
            workdir='./'
        )

    def __str__(self):
        """
        String representation of the class object
        """
        return self.__class__.__name__

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{self.__class__.__name__} v{self.version} (Layer {layer}) started on @{me.username}.")

    async def stop(self, *args):
        """
        Stop function
        :param args:
        """
        await super().stop()
        print(f"{self.__class__.__name__} stopped. Bye.")

    def admins(self):
        return ast.literal_eval(self.config.get('bot', 'admins'))

    def is_admin(self, entity: Message or CallbackQuery) -> bool:
        user_id = entity.from_user.id

        return user_id in self.admins()

    @staticmethod
    def admins_only(func):
        @wraps(func)
        async def decorator(bot: BmlFireflyBot, message: Message):
            if bot.is_admin(message):
                await func(bot, message)

        decorator.admin = True

        return decorator

    async def send_log(
            self,
            text: str,
            parse_mode: Optional[str] = object,
            entities: List["types.MessageEntity"] = None,
            disable_web_page_preview: bool = None,
            disable_notification: bool = None,
            reply_to_message_id: int = None,
            schedule_date: int = None,
            reply_markup: Union[
                "types.InlineKeyboardMarkup",
                "types.ReplyKeyboardMarkup",
                "types.ReplyKeyboardRemove",
                "types.ForceReply"
            ] = None
    ) -> Union["types.Message", None]:
        """ Send Message to log group. """
        chat_id = self.config.get(self.name, 'log_group', fallback=None)

        if chat_id:
            return await self.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, entities=entities,
                                           disable_web_page_preview=disable_web_page_preview,
                                           disable_notification=disable_notification,
                                           reply_to_message_id=reply_to_message_id, schedule_date=schedule_date,
                                           reply_markup=reply_markup)

        return None

    async def send_log_document(
            self,
            document: Union[str, BinaryIO],
            thumb: Union[str, BinaryIO] = None,
            caption: str = "",
            parse_mode: Optional[str] = object,
            caption_entities: List["types.MessageEntity"] = None,
            file_name: str = None,
            force_document: bool = None,
            disable_notification: bool = None,
            reply_to_message_id: int = None,
            schedule_date: int = None,
            reply_markup: Union[
                "types.InlineKeyboardMarkup",
                "types.ReplyKeyboardMarkup",
                "types.ReplyKeyboardRemove",
                "types.ForceReply"
            ] = None,
            progress: callable = None,
            progress_args: tuple = ()
    ) -> Union["types.Message", None]:
        """ Send Message to log group. """
        chat_id = self.config.get(self.name, 'log_group', fallback=None)

        if chat_id:
            return await self.send_document(chat_id=chat_id, document=document, thumb=thumb, caption=caption,
                                            caption_entities=caption_entities, file_name=file_name,
                                            force_document=force_document, parse_mode=parse_mode,
                                            reply_to_message_id=reply_to_message_id, schedule_date=schedule_date,
                                            reply_markup=reply_markup, progress=progress, progress_args=progress_args)

        return None

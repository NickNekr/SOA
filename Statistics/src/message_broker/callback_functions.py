from datetime import datetime
import pickle

from database.session import get_session_outside_depends
from database.model import Views, Likes, LikesStats, ViewsStats
from tools.repo_alchemy_linker import get_mono_repos

mono_repos = get_mono_repos()

async def views_callback(msg):
    await mono_repos.ProduceEntity(msg, Views)

async def likes_callback(msg):
    await mono_repos.ProduceEntity(msg, Likes)

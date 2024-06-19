import pytest
import grpc
from unittest.mock import Mock, patch

from TasksService.src.tasks_service.routers import task_exist
from TasksService.src.config import Config, get_config

@pytest.mark.asyncio
async def test_task_exist():
    task = Mock()
    context = Mock()
    assert task_exist(task, context) is True
    context.set_code.assert_not_called() 

    task = None
    context = Mock()
    assert task_exist(task, context) is False
    context.set_code.assert_called_once_with(grpc.StatusCode.NOT_FOUND)  
    context.set_details.assert_called_once_with("Task not found")  



@patch('TasksService.src.config.Config', autospec=True)
def test_get_config_cache(mock_config):
    config1 = get_config()
    config2 = get_config()

    mock_config.assert_called_once()

    assert config1 is config2
    assert isinstance(config1, Config)


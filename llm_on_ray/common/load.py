#
# Copyright 2023 The LLM-on-Ray Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
from typing import Any, Dict

from llm_on_ray.common import logger
from llm_on_ray.common import agentenv, dataset, initializer, model, optimizer, tokenizer, trainer


def load_check_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"{func.__name__} start")
            ret = func(*args, **kwargs)
        except Exception as e:
            logger.critical(f"{func.__name__}: {e}", exc_info=True)
            exit(1)
        logger.info(f"{func.__name__} finish")
        if ret is None:
            logger.critical(f"{func.__name__} has wrong return type")
            exit(1)
        else:
            return ret

    return wrapper


@load_check_decorator
def load_dataset(config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    datasets_type = config.get("type", None)
    Factory = dataset.Dataset.registory.get(datasets_type)
    if Factory is None:
        raise ValueError(f"there is no {datasets_type} dataset.")
    else:
        try:
            _ = Factory()(config)
        except Exception as e:
            logger.critical(f"{Factory.__name__} call error: {e}", exc_info=True)
            exit(1)
        return _


@load_check_decorator
def load_tokenizer(config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    tokenizer_type = config.get("type", None)
    Factory = tokenizer.Tokenizer.registory.get(tokenizer_type)
    if Factory is None:
        raise ValueError(f"there is no {tokenizer_type} tokenizer.")
    else:
        try:
            _ = Factory()(config)
        except Exception as e:
            logger.critical(f"{Factory.__name__} call error: {e}", exc_info=True)
            exit(1)
        return _


@load_check_decorator
def load_model(config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    model_type = config.get("type", None)
    Factory = model.Model.registory.get(model_type)
    if Factory is None:
        raise ValueError(f"there is no {model_type} model.")
    else:
        try:
            _ = Factory()(config)
        except Exception as e:
            logger.critical(f"{Factory.__name__} call error: {e}", exc_info=True)
            exit(1)
        return _


@load_check_decorator
def load_optimizer(model, config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    optimizer_type = config.get("type", None)
    Factory = optimizer.Optimizer.registory.get(optimizer_type)
    if Factory is None:
        raise ValueError(f"there is no {optimizer_type} optimizer.")
    else:
        try:
            _ = Factory()(model, config)
        except Exception as e:
            logger.critical(f"{Factory.__name__} call error: {e}", exc_info=True)
            exit(1)
        return _


@load_check_decorator
def get_trainer(config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    trainer_type = config.get("type", None)
    Factory = trainer.Trainer.registory.get(trainer_type)
    if Factory is None:
        raise ValueError(f"there is no {trainer_type} trainer.")
    try:
        _ = Factory(config)
    except Exception as e:
        logger.critical(f"{Factory.__name__} init error: {e}", exc_info=True)
        exit(1)
    return _


@load_check_decorator
def get_initializer(config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    initializer_type = config.get("type", None)
    Factory = initializer.Initializer.registory.get(initializer_type)
    if Factory is None:
        raise ValueError(f"there is no {initializer_type} initializer.")
    try:
        _ = Factory(config)
    except Exception as e:
        logger.critical(f"{Factory.__name__} init error: {e}", exc_info=True)
        exit(1)
    return _


@load_check_decorator  # type: ignore # noqa: F405 # may be undefined, or defined from star imports
def get_agentenv(config: Dict[str, Any]):
    logger.info(f"{sys._getframe().f_code.co_name} config: {config}")
    agentenv_type = config.get("type", None)
    Factory = agentenv.AgentEnv.registory.get(agentenv_type)
    if Factory is None:
        raise ValueError(f"there is no {agentenv_type} AgentEnv.")
    try:
        _ = Factory(config)
    except Exception as e:
        logger.critical(f"{Factory.__name__} init error: {e}", exc_info=True)
        exit(1)
    return _

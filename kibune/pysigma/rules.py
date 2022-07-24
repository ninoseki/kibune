from functools import lru_cache

import yaml

from kibune.core import settings
from kibune.pysigma import schemas
from kibune.pysigma.factories import RuleFactory


@lru_cache(maxsize=settings.SIGMA_RULE_CACHE_SIZE)
def load_rule(rule_str: str) -> schemas.Rule:
    """
    Load a single sigma signature from a file object

    :param signature_file: a file like object containing sigma yaml
    :return: Signature object
    """
    data = yaml.safe_load(rule_str)
    return RuleFactory.from_data(data=data)

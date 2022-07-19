import yaml

from kibune.pysigma import schemas
from kibune.pysigma.factories import RuleFactory


def load_rule(rule_str: str) -> schemas.Rule:
    """
    Load a single sigma signature from a file object

    TODO introduce caching at this layer?

    :param signature_file: a file like object containing sigma yaml
    :return: Signature object
    """
    data = yaml.safe_load(rule_str)
    return RuleFactory.from_data(data=data)

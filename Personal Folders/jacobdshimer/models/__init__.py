from enum import Enum

from pydantic import BaseModel


class TaxonomicType(str, Enum):
    kingdom = 'kingdom'
    phylum = 'phylum'
    _class = 'class'
    order = 'order'
    family = 'family'
    genus = 'genus'


class TaxonomicRank(BaseModel):
    type: TaxonomicType

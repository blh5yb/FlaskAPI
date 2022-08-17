from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional


#class GeneModel(BaseModel):
#    geneSymbol: str
#    geneId: str
#    geneFullName: Optional[str]


class VariantSaveModel(BaseModel):
    chr: str
    pos: int
    ref: str
    alt: str
    quality: Optional[float]
    #gene: GeneModel

    @validator('chr')
    def chr_check(cls, v):
        allowed_ids = [str(i) for i in range(1, 23)]
        allowed_ids.extend(['X', 'Y'])
        allowed_chr = ['chr' + i for i in allowed_ids]
        if v not in allowed_chr:
            raise ValueError('chr value is not allowed')
        return v

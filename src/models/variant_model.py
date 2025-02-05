from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

variant_types = {
    "SUBSTITUTION": True,
    "INSERTION": True,
    "DELETION": True,
    "DELIN": True,
    "COPY_NUMBER": True,
    "FUSION": True,
    "TANDEM_DUPLICATION": True
}

#class GeneModel(BaseModel):
#    geneSymbol: str
#    geneId: str
#    geneFullName: Optional[str]


class VariantModel(BaseModel):
    chr: str #db.StringField(required=True)
    pos: int
    ref: str
    alt: str
    variant_type: str
    quality: Optional[float]
    created_at: Optional[datetime] = datetime.utcnow() #
    updated_at: Optional[datetime] = datetime.utcnow()
    #gene: GeneModel

    # custom validators
    @validator('variant_type')
    def var_type_check(cls, v):
        print('vartype valid', v, variant_types[v])
        if not variant_types[v.upper()]:
            raise ValueError(f'variant_type is not allow. Must be one of ${variant_types.keys()}')

        return v

    @validator('chr')
    def chr_check(cls, v):
        allowed_chr = {f'chr{i}': True for i in range(1, 23)}
        allowed_chr['chrX'] = True
        allowed_chr['chrY'] = True
        if not allowed_chr[v]:
            raise ValueError('chr value is not allowed')
        return v

from uuid import uuid4

from sqlalchemy import (
    VARCHAR,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    Integer,
    Boolean,
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy_utils import LtreeType

from app.database import Base
from app.errors import CheckFieldError


class AssociationTaxonomyJob(Base):
    __tablename__ = "association_taxonomy_job"

    taxonomy_id = Column(
        VARCHAR,
        ForeignKey("taxonomy.id", ondelete="cascade"),
        primary_key=True
    )
    job_id = Column(VARCHAR, primary_key=True)


class Taxonomy(Base):
    __tablename__ = "taxonomy"

    id = Column(
        VARCHAR, primary_key=True, default=lambda: uuid4().hex
    )
    name = Column(VARCHAR, nullable=False)
    version = Column(Integer, nullable=False)
    tenant = Column(VARCHAR, nullable=True)
    # TODO
    category_id = Column(VARCHAR, nullable=False)
    taxons = relationship("Taxon", back_populates="taxonomy")
    latest = Column(Boolean, nullable=False)


class Taxon(Base):
    __tablename__ = "taxon"

    id = Column(
        VARCHAR, primary_key=True, default=lambda: uuid4().hex
    )
    name = Column(VARCHAR, nullable=False)
    tenant = Column(VARCHAR, nullable=True)
    taxonomy_id = Column(
        VARCHAR,
        ForeignKey("taxonomy.id"),
        nullable=False,
        index=True,
    )
    taxonomy = relationship(
        "Taxonomy",
        back_populates="taxons",
    )
    parent_id = Column(
        VARCHAR,
        ForeignKey("taxon.id", ondelete="cascade"),
        CheckConstraint("id != parent_id", name="self_parent_id_const"),
        nullable=True,
        index=True,
    )
    parent = relationship(
        "Taxon",
        remote_side=[id],
    )
    tree = Column(LtreeType, nullable=True)
    __table_args__ = (
        Index("index_taxon_tree", tree, postgresql_using="gist"),
    )

    @validates("id")
    def validate_id(self, key, id_):
        if id_ and not id_.replace('_', '').isalnum():
            raise CheckFieldError("Taxon id must be alphanumeric.")
        return id_

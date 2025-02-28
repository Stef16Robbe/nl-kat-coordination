"""Add index on BoefjeMeta table: organization_boefje_id

Revision ID: fa64454868a9
Revises: ebc7de8be4e3
Create Date: 2023-03-29 08:23:08.521462

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "fa64454868a9"
down_revision = "ebc7de8be4e3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_boefje_meta_organization_boefje_id", "boefje_meta", ["organization", "boefje_id"], unique=False)
    op.create_index(op.f("ix_normalizer_meta_raw_file_id"), "normalizer_meta", ["raw_file_id"], unique=False)
    op.create_index(op.f("ix_raw_file_boefje_meta_id"), "raw_file", ["boefje_meta_id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_boefje_meta_organization_boefje_id", table_name="boefje_meta")
    op.drop_index(op.f("ix_raw_file_boefje_meta_id"), table_name="raw_file")
    op.drop_index(op.f("ix_normalizer_meta_raw_file_id"), table_name="normalizer_meta")
    # ### end Alembic commands ###

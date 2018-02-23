#!/usr/bin/python
# coding=UTF-8

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData

engine = create_engine('postgresql://knightstalker:opendata2017@localhost/e193')
results_per_page = 50

metadata = MetaData()
# Only these tables, mainly "ocorrencias" and its dependencies
metadata.reflect(engine, only = [
    'ocorrencias',
    'cidades',
    'bairros',
    'logradouros',
    'ocorrencia_evento_orgao',
    'evento_orgao',
    'viaturas',
    'empenho_viaturas',
    'efetivo',
    'historico_atendimento'
    ]
)
Base = automap_base(metadata = metadata)
Base.prepare()

Session = sessionmaker(bind = engine)
session = Session()

Ocorrencias = Base.classes.ocorrencias
Cidades = Base.classes.cidades
Bairros = Base.classes.bairros
Logradouros = Base.classes.logradouros
Ocorrencia_evento_orgao = Base.classes.ocorrencia_evento_orgao
Evento_orgao = Base.classes.evento_orgao
Viaturas = Base.classes.viaturas
Empenho_viaturas = Base.classes.empenho_viaturas
Efetivo = Base.classes.efetivo
Historico_atendimento = Base.classes.historico_atendimento

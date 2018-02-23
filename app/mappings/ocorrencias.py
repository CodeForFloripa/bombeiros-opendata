#!/usr/bin/python
# coding=UTF-8

import json
from flask_restful import Resource, reqparse
import database

class CustomDatetimeSerializer(json.JSONEncoder):
    """Na especificação do Json não tem um tipo 'DateTime'. Vai entender."""
    def default(self, stuff):
        if hasattr(stuff, 'isoformat'):
            return stuff.isoformat(' ')
        return json.JSONEncoder.default(self, stuff)

def get_ocorrencia_as_dict(id_o):
    """ Busca pela ocorrência com id_ocorrencia, e retorna um dict."""
    session = database.session
    ocorrencia = session.query(database.Ocorrencias).filter_by(id_ocorrencia = id_o).first()
    result = {
        'latitude' : None,
        'longitude' : None,
        'id' : ocorrencia.id_ocorrencia,
        'ts' : ocorrencia.ts_ocorrencia,
        'descricao' : ocorrencia.de_inicial,
        'bairro' : ocorrencia.nm_bairro_prv,
        'logradouro' : ocorrencia.nm_logradouro_prv,
        'numero' : ocorrencia.nr_edificacao,
        # 'complemento' : ocorrencia.complemento_prv,
        'complemento' : None,
        'referencia' : ocorrencia.nm_referencia,
        'cidade' : {
            'id' : ocorrencia.cidades.id_cidade,
            'nome' : ocorrencia.cidades.nm_cidade
        },
        'tipoEmergencia' : {
                'id' : ocorrencia.tp_emergencia.id_tp_emergencia,
                'nome' : ocorrencia.tp_emergencia.nm_tp_emergencia
        },
        'listViatura' : []
    }
    empenhos = session.query(database.Empenho_viaturas).\
            filter_by(id_ocorrencia = ocorrencia.id_ocorrencia).all()
    for empenho in empenhos:
        try:
            historico_atendimento = \
                session.query(database.Historico_atendimento).\
                        filter_by(id_ocorrencia = ocorrencia.id_ocorrencia,
                                id_viatura = empenho.viaturas.id_viatura).\
                                        first()
        except:
            historico_atendimento = None

        viatura = {
                'id' :
                    empenho.viaturas.id_viatura,
                'nome' :
                    empenho.viaturas.id_viatura,
                'ts_empenho' :
                    empenho.dt_tm_empenho,
                'ts_saida_base' :
                    # empenho.dt_tm_sai_base,
                    None,
                'ts_chegada_ocorrencia' :
                    empenho.dt_tm_chg_ocor,
                'ts_saida_ocorrencia' :
                    empenho.dt_tm_sai_ocor,
                'ts_chegada_intermediaria' :
                    empenho.dt_tm_chg_inter,
                'ts_saida_intermediaria' :
                    empenho.dt_tm_sai_inter,
                'ts_chegada_base' :
                    # empenho.dt_tm_base,
                    None,
                'ts_envio_samu' :
                    empenho.dt_tm_envio_samu,
            }
        if historico_atendimento:
            viatura['historicoAtendimento'] = {
                    'id' :
                        historico_atendimento.id_ts_historico_atendimento,
                    'ts' :
                        historico_atendimento.id_ts_historico_atendimento,
                    'bairro':
                        ocorrencia.nm_bairro_prv,
                    'logradouro' :
                        ocorrencia.nm_logradouro_prv,
                    'numero':
                        ocorrencia.nr_edificacao,
                    'complemento':
                        None,
                    'referencia':
                        ocorrencia.nm_referencia,
                    'tipoEmergencia' : {
                        'id' : ocorrencia.tp_emergencia.id_tp_emergencia,
                        'nome' : ocorrencia.tp_emergencia.nm_tp_emergencia
                    }
            }
            viatura['historicoAtendimento']['listOrgaoApoio'] = None
            orgaos_apoio = session.query(database.Ocorrencia_evento_orgao).\
                filter_by(id_ocorrencia = ocorrencia.id_ocorrencia).all()
            if orgaos_apoio:
                orgaos = []
                for orgao in orgaos_apoio:
                    orgaos.append(
                        {
                            'id' : orgao.evento_orgao.id_orgao_apoio,
                            'nome' : orgao.evento_orgao.ds_orgao_apoio
                        }
                    )
                    viatura['historicoAtendimento']['listOrgaoApoio'] = orgaos
        else:
            viatura['historicoAtendimento'] = None
        result['listViatura'].append(viatura)
    return result

class Ocorrencia(Resource):
    def get(self, id_ocorrencia):
        return json.dumps(get_ocorrencia_as_dict(id_ocorrencia), cls=CustomDatetimeSerializer)

class ListarOcorrencias(Resource):
    def __init__(self):
        self.result = None

    def check_database(self):
        try:
            session = database.session
            session.execute('SELECT 1')
            return True
        except:
            session.close()
            return False

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('pagina', type = int)
        args = parser.parse_args()

        if 'pagina' in args.keys():
            page = args['pagina']
        else:
            page = 1

        session = database.session
        ocorrencias_q = session.query(database.Ocorrencias).\
                order_by(database.Ocorrencias.id_ocorrencia.desc())
        ocorrencias_q = ocorrencias_q.limit(database.results_per_page)
        ocorrencias_q = ocorrencias_q.offset(page)
        results = []

        if self.check_database():
            for ocorrencia in ocorrencias_q:
                results.append(get_ocorrencia_as_dict(ocorrencia.id_ocorrencia))

        return json.dumps(results, cls=CustomDatetimeSerializer)

#!/usr/bin/python
# coding=UTF-8

from flask import Flask
from flask_restful import Api, Resource, reqparse

from mappings.ocorrencias import ListarOcorrencias, Ocorrencia

if __name__ == '__main__':
    app = Flask(__name__)
    api = Api(app)

    app.config['ERROR_404_HELP'] = False

    api.add_resource(ListarOcorrencias, '/ocorrencias', endpoint = 'ocorrencias')
    api.add_resource(Ocorrencia, '/ocorrencias/<int:id_ocorrencia>', endpoint = 'ocorrencia')

    #app.run(debug = True)
    app.run(host='0.0.0.0', port=5000, debug=True)

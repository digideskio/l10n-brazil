# -*- coding: utf-8 -*-

##############################################################################
#                                                                            #
#  Copyright (C) 2012 Proge Informática Ltda (<http://www.proge.com.br>).    #
#                                                                            #
#  Author Daniel Hartmann <daniel@proge.com.br>                              #
#                                                                            #
#  This program is free software: you can redistribute it and/or modify      #
#  it under the terms of the GNU Affero General Public License as            #
#  published by the Free Software Foundation, either version 3 of the        #
#  License, or (at your option) any later version.                           #
#                                                                            #
#  This program is distributed in the hope that it will be useful,           #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU Affero General Public License for more details.                       #
#                                                                            #
#  You should have received a copy of the GNU Affero General Public License  #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                            #
##############################################################################

from osv import osv, fields
from tools.translate import _
import re


class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'natureza_juridica_id': fields.many2one(
            'l10n_br.natureza_juridica', u'Natureza Jurídica', required=True
            ),
        'porte_id': fields.many2one('l10n_br.porte', u'Porte', required=True),
        'optante_simples_nacional': fields.boolean(
            u'Optante pelo Simples Nacional'
            ),
        'participa_pat': fields.boolean(
            u'Participa do Programa de Alimentação do Trabalhador (PAT)'
            ),
        'responsavel_legal_id': fields.many2one(
            'res.partner', u'Responsável Legal', required=True,
            ),
        'legal_name' : fields.char(
            u'Razão Social', size=128, required=True,
            help=u'Nome utilizado em documentos fiscais'
            ),
        'cnpj': fields.char(u'CNPJ', size=18, required=True),
        'inscr_est': fields.char(u'Inscr. Estadual', size=16),
        'inscr_mun': fields.char(u'Inscr. Municipal', size=18),
        'suframa': fields.char(u'Suframa', size=18),
        }

    def _validate_cnpj(self, cr, uid, ids):
        company = self.browse(cr, uid, ids[0])
        if not company.cnpj:
            return True

        cnpj = company.cnpj

        if not cnpj.isdigit():
            cnpj = re.sub('[^0-9]', '', cnpj)

        if len(cnpj) != 14:
            return False

        cnpj = map(int, cnpj)
        novo = cnpj[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(novo) < 14:
            r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
            prod.insert(0, 6)

        if novo == cnpj:
            return True

        return False

    _constraints = [
        (_validate_cnpj, u'CNPJ inválido.', ['cnpj']),
        ]

    def onchange_mask_cnpj(self, cr, uid, ids, cnpj):
        if not cnpj:
            return {}
        val = re.sub('[^0-9]', '', cnpj)

        if len(val) >= 14:
            cnpj = "%s.%s.%s/%s-%s" % (val[0:2], val[2:5], val[5:8], val[8:12], val[12:14])

        return {'value': {'cnpj': cnpj}}


res_company()
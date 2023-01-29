import matplotlib
import receipt_wrappers as rw
import numpy as np
import gurobipy as gp
from scipy.optimize import linprog
import matplotlib.pyplot as plt

class Matching:
    data_folder_path = ''
    users_df = None

    receipts = []
    receipt_did = []
    receipts_users = []
    receipt_users_did = []
    receipts_ocr = []
    receipt_ocr_did = []

    param_names = []
    param_coefs = []
    edge_names = []
    multi_edge_weights = {}
    simple_edge_weights_vector = []

    mdl = None
    mdl_vars = None

    def __init__(self, data_folder_path, users_df):
        self.data_folder_path = data_folder_path
        self.users_df = users_df
        self.receipts = rw.Receipt.initialize_batch_receipts(self.data_folder_path, self.users_df)
        self.receipt_did = [rec.doc_id for rec in self.receipts]
        self.receipts_users = [rec for rec in self.receipts if rec.has_user]
        self.receipt_users_did = [rec.doc_id for rec in self.receipts_users]
        self.receipts_ocr = [rec for rec in self.receipts if rec.has_ocr]
        self.receipt_ocr_did = [rec.doc_id for rec in self.receipts_ocr]
        self.simple_edge_weights_vector = []
        for user_rec in self.receipts_users:
            for ocr_rec in self.receipts_ocr:
                edge_name = self.get_edge_name(user_rec, ocr_rec)
                self.edge_names.append(edge_name)
                self.multi_edge_weights[edge_name] = []

    def get_edge_name(self, user_rec, ocr_rec):
        return tuple([user_rec.doc_id, ocr_rec.doc_id])

    def add_edge_weight(self, edge_to_weight_function, p_name='', p_coef=1):
        self.param_names.append(p_name)
        self.param_coefs.append(p_coef)
        for user_rec in self.receipts_users:
            for ocr_rec in self.receipts_ocr:
                edge_name = self.get_edge_name(user_rec, ocr_rec)
                wgt = edge_to_weight_function(user_rec, ocr_rec)
                self.multi_edge_weights[edge_name].append(wgt)

    def compute_simple_edge_weights_vector(self):
        n_param = len(self.param_coefs)
        self.simple_edge_weights_vector = []
        for edge_name in self.edge_names:
            wgt = sum([self.param_coefs[ind] * self.multi_edge_weights[edge_name][ind] for ind in range(n_param)])
            self.simple_edge_weights_vector.append(wgt)
        plt.hist(self.simple_edge_weights_vector)
        plt.show()

    def solve_bipartite_matching(self):
        obj = [-1 * wgt for wgt in self.simple_edge_weights_vector]


        # A = [[0] * len(self.edge_names)] * len(self.receipt_did)
        A = np.zeros(shape=(len(self.receipt_users_did) + len(self.receipt_ocr_did), len(self.edge_names)))
        for edge_ind in range(len(self.edge_names)):
            # print('-' * 10)
            # print(edge_ind)
            edge = self.edge_names[edge_ind]
            user_ind = self.receipt_users_did.index(edge[0])
            ocr_ind = self.receipt_ocr_did.index(edge[1])
            # print(ocr_ind)
            # A[user_ind][edge_ind] = 1
            # A[ocr_ind][edge_ind] = 2
            A[user_ind, edge_ind] = 1
            A[len(self.receipt_users_did) + ocr_ind, edge_ind] = 1

        print(A)
        print(len(A.tolist()))
        print(len(A.tolist()[0]))
        print(np.sum(A, axis=1))
        print(np.sum(A, axis=0))
        print(np.mean(np.sum(A, axis=0)))
        print(len(np.sum(A, axis=1)))
        print(len(np.sum(A, axis=0)))
        print(A.shape)
        # print(A[0])
        # print(len(A))
        # print(len(A[0]))
        

        b = [1] * (len(self.receipt_users_did) + len(self.receipt_ocr_did))
        
        res = linprog(obj, A_ub=A, b_ub=b, bounds=[0, 1])

        print(res.x)
        print(res.x[0])
        print(res.fun)
        print(res.status)
        
        soln_matches = [self.edge_names[ind] for ind in range(len(self.edge_names)) if res.x[ind] > 0.9]
        soln_hits = [edge[0] for edge in soln_matches if edge[0] == edge[1]]
        soln_accuracy = len(soln_hits) / len(self.receipts_users)
        print([res.x[ind] for ind in range(len(self.edge_names)) if res.x[ind] > 0.01])
        plt.hist([res.x[ind] for ind in range(len(self.edge_names))])
        plt.show()

        return soln_matches, soln_hits, soln_accuracy

    # def solve_bipartite_matching(self):
    #     self.mdl = gp.Model('primal')
    #     # self.mdl.setParam('OutputFlag', False)

    #     self.match_vars = self.mdl.addVars(self.edge_names, name='match_edge', lb=0)

    #     self.mdl.setObjective(gp.LinExpr(self.simple_edge_weights_vector, self.match_vars.select('*')), gp.GRB.MAXIMIZE)

    #     users_did = [rec.doc_id for rec in self.receipts_users]
    #     ocr_did = [rec.doc_id for rec in self.receipts_ocr]


    #     self.mdl.addConstrs(gp.quicksum(self.match_vars[(user, ocr)] for user in users_did)
    #                 <= 1
    #                 for ocr in ocr_did)

    #     self.mdl.addConstrs(gp.quicksum(self.match_vars[(user, ocr)] for ocr in ocr_did)
    #                 <= 1
    #                 for user in users_did)

    #     self.mdl.optimize()

    # def report_solution(self):
    #     if self.mdl.status != 2:
    #         raise Exception('mdl attribute not optimized.')
        
    #     soln_matches = [edge for edge in self.edge_names if self.match_vars[edge].X > 0.99]
    #     soln_hits = [edge[0] for edge in soln_matches if edge[0] == edge[1]]
    #     soln_accuracy = len(soln_hits) / len(self.receipts_users)

    #     print([self.match_vars[edge].X for edge in self.edge_names])
    #     print(sum([self.match_vars[edge].X for edge in self.edge_names]))

    #     plt.hist([self.match_vars[edge].X for edge in self.edge_names])
    #     plt.show()

    #     return soln_matches, soln_hits, soln_accuracy

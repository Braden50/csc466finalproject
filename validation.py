from Data import Data
import copy
import sys
from classify import classify_data
from InduceC45 import algorithm_c45, Node
import pandas as pd
def cross_evaluation(d: Data, threshold: float , k: int, gain_ratio : bool):

    total_length = len(d.data)
    if k == 0 or k == 1:
        folds = 0
        k = 1
    elif k == -1:
        folds = 1
        k = total_length
    else:
        folds = total_length // k
    map_result = []
    i = 0
    while i < k:
        copy_d = copy.deepcopy(d)
        excluded_copy_d = copy.deepcopy(d)
        data_copy_d = copy_d.data
        if i == k - 1:
            excluded_d = data_copy_d[i * folds:]
        else:

            excluded_d = data_copy_d[i*folds : i*folds + folds]
        new_d = data_copy_d[0 : i * folds ] + data_copy_d[i * folds + folds: ]
        copy_d.data = new_d
        excluded_copy_d.data = excluded_d

        head_node = Node('')
        algorithm_c45(copy_d, copy_d.data, copy_d.attributes, float(threshold), head_node, gain_ratio)
        final_json = {'dataset': filename,
                      'node': head_node.__dict__}

        classified_result = {}
        if folds != 0:
            if final_json['node'] and final_json['node']['var'] != '':
                classified_result = classify_data(excluded_copy_d, final_json['node'])
        else:
            if final_json['node'] and final_json['node']['var'] != '':
                classified_result = classify_data(copy_d, final_json['node'])

        classified_result = list(classified_result.values())
        for result in classified_result:
            map_result.append(result)
        i += 1
    return map_result

if __name__ == '__main__':


    filename = "newTrails.csv"
    threshold = 0.05
    k = 10
    gain_ratio = False
    try:
        restricted_file = sys.argv[5]
        file_reader = open(restricted_file, 'r')
        line = file_reader.readline()
        line = line.strip('\n')
        line = line.replace(' ', '')
        optional_file = line.split(',')
    except:
        optional_file = []
    omitted_attributes = []
    for index, value in enumerate(optional_file):
        if value == '0':
            omitted_attributes.append(index)
    data = Data(filename, omitted_attributes)
    actual_result = list(map(lambda x: x[data.index_class_variable], data.data))
    cross_evaluation_result = cross_evaluation(data,threshold, k, gain_ratio)
    matched_value = 0
    average_accuracy = {}
    fold_number = 1
    if k == -1:
        k = 1
    for i in range(len(cross_evaluation_result)):
        if cross_evaluation_result[i] == actual_result[i]:
            matched_value += 1
        if k != 0 and k != 1:
            if (i + 1) % k == 0:
                if fold_number != k:
                    fold_predicted_value = cross_evaluation_result[i + 1 - k:i + 1]
                    fold_actual_result = actual_result[i + 1 - k : i + 1 ]
                else:
                    fold_predicted_value = cross_evaluation_result[i + 1 - k:]
                    fold_actual_result = actual_result[i + 1 - k:]
                fold_matched = 0
                for j in range(len(fold_predicted_value)):
                    if fold_predicted_value[j] == fold_actual_result[j]:
                        fold_matched += 1
                average_accuracy[fold_number] = fold_matched / len(fold_predicted_value)
                fold_number += 1


    y_actu = pd.Series(actual_result, name='Actual')
    y_pred = pd.Series(cross_evaluation_result, name='Predicted')
    df_confusion = pd.crosstab(y_actu, y_pred, rownames=['Actual'], colnames=['Predicted'], margins=True)
    print(df_confusion)
    print('Predicted {0} correct out of {1} predictions -- \nOverall Accuracy = {2}'.format(matched_value,len(cross_evaluation_result), matched_value/len(cross_evaluation_result)))
    try:
        if k != 0 and k != 1:
            print('Average Accuracy across all folds = {0}'.format(sum(average_accuracy.values())/len(average_accuracy.values())))
        else:
            print('Average Accuracy across all folds = {0}'.format(matched_value/len(cross_evaluation_result)))

    except:
        print('Average Accuracy across all folds = 0 ')
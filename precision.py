import os


def iou(box1, box2):
    '''
    两个框（二维）的 iou 计算

    注意：边框以左上为原点

    box:[x1,y1,x2,y2],依次为左上右下坐标
    '''
    h = max(0, min(box1[2], box2[2]) - max(box1[0], box2[0]))
    w = max(0, min(box1[3], box2[3]) - max(box1[1], box2[1]))
    area_box1 = ((box1[2] - box1[0]) * (box1[3] - box1[1]))
    area_box2 = ((box2[2] - box2[0]) * (box2[3] - box2[1]))
    inter = w * h
    union = area_box1 + area_box2 - inter
    iou = inter / union
    return iou

def read_boxs(truth_txt_path, predict_txt_path,model_name):
    output_pred_boxs = []
    truth_boxs = []
    if model_name == 'Retina_Face_label_moblie' or model_name == 'Retina_Face_label_rest50':
        with open(truth_txt_path, 'r') as f_truth, open(predict_txt_path, 'r') as f_pre:
            truth_boxs = f_truth.readlines()
            pred_boxs = f_pre.readlines()
            for pred_box in pred_boxs:
                pred_box = pred_box.split()[:-1]
                output_pred_boxs.append(pred_box)

    elif model_name == 'yolo_face_v2_label':
        with open(truth_txt_path,'r') as f_truth, open(predict_txt_path,'r') as f_pre:
            for _ in range(2):
                next(f_pre)
            truth_boxs = f_truth.readlines()
            pred_boxs = f_pre.readlines()
            for pred_box in pred_boxs:
                pred_box = pred_box.split()[:-1]
                pred_box[2] = float(pred_box[0]) + float(pred_box[2])
                pred_box[3] = float(pred_box[1]) + float(pred_box[3])
                output_pred_boxs.append(pred_box)

    return truth_boxs, output_pred_boxs


def computer_precision_recall(truth_txt_path, predict_txt_path,model_name,iou_them = 0.5):
    pred_iou = []
    TP = 0
    FP = 0

    truth_boxs,pred_boxs = read_boxs(truth_txt_path,predict_txt_path,model_name)

    for pred_box in pred_boxs:
        max_iou = 0.0
        for truth_box in truth_boxs:
            truth_box = truth_box.split()
            pred_box = list(map(float, pred_box))
            truth_box = list(map(float, truth_box))
            if max_iou < iou(pred_box,truth_box):
                max_iou = iou(pred_box,truth_box)

        pred_iou.append(max_iou)


    for i in pred_iou:
        if i >= iou_them:
            TP += 1
        else:
            FP += 1

    return float(TP / (TP + FP) * 1.0),float(TP / len(truth_boxs)*1.0)



dir_path = 'F:\huawei_data\HWtestdataset_stage_label'
# xml2txt(dir_path)
file_names = os.listdir(dir_path+'\\txt_label')

# try:
models_name = ['Retina_Face_label_moblie','Retina_Face_label_rest50','yolo_face_v2_label']
for model_name in models_name:
    precisions_sum = {}
    video_lens = {}
    recall_sum = {}
    for file_name in file_names:
        file_split_name = file_name.split('_')
#---------------------------------------------输出的单张precision------------------------------------------------
        # with open(dir_path + '\\' + model_name + '.txt', 'w') as f:
        #     f.write('picture_name' + ' ' + 'precision' + '\n')
        #     precision = computer_precision(dir_path+'\\txt_label\\' + file_name,dir_path+'\\'+model_name+'_label\\' + file_name)
        #     f.write(file_name + '\t' + str(precision)+'\n')
        #     # print(file_name+' '+ str(precision))
#-----------------------------------------------------------------------------------------------------------------

        if file_split_name[0] not in precisions_sum:
            precisions_sum[file_split_name[0]] = 0.0
            video_lens[file_split_name[0]] = 0
            recall_sum[file_split_name[0]] = 0.0


        precision,recall = computer_precision_recall(dir_path+'\\txt_label\\' + file_name,dir_path+'\\'+model_name+'\\' + file_name,model_name)
        video_lens[file_split_name[0]] += 1
        precisions_sum[file_split_name[0]] += precision
        recall_sum[file_split_name[0]] += recall

#-------------------------------------------------按照视频输出precision和recall-------------------------------------
    priecision_float_sum = 0.0
    recall_float_sum = 0.0
    with open(dir_path + '\\' + model_name + '.txt', 'w') as f:
        f.write('picture' + '\t'+ 'number' +'\t' + 'precision' + '\t' + 'recall'+'\n')
        for k, v in precisions_sum.items():
            priecision_float_sum += v
            recall_float_sum += recall_sum[k]
            f.write("{}\t\t{}\t{:.6f}\t{:.6f}\n".format(k , video_lens[k], v / video_lens[k] * 1.0 , recall_sum[k]/video_lens[k] * 1.0))
            print(k + '\t' + str(v / video_lens[k] * 1.0) + '\t' + str(recall_sum[k]/video_lens[k] * 1.0))

        f.write("{}\t\t{:.6f}\t{:.6f}\n".format('total ans' ,
                priecision_float_sum / sum(video_lens.values()) * 1.0,
                recall_float_sum / sum(video_lens.values()) * 1.0))
        print('total ans' + '\t' +
              str(priecision_float_sum / sum(video_lens.values()) * 1.0) + '\t' +
              str(recall_float_sum / sum(video_lens.values()) * 1.0))
#---------------------------------------------------------------------------------------------------------
# except:
#     print(file_name)
#     print(model_name)
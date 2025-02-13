import torch
from test import test
from net import Net
from variables import *
import matplotlib.pyplot as plt

def load_network():
    network_state = torch.load("/Users/mayabasu/PycharmProjects/MNIST-test-neural-net2/neuralnets/model.pth")
    network = Net()
    network.load_state_dict(network_state)
    return network





def make_roc_curve(cutoffs, network,filepath):

    false_positives = []
    true_positives = []


    for i in range(len(cutoffs)):


        hits, correct, test_losses,num_times_signal_was_missed,num_times_signal_was_contaminated,num_times_signal_appears_in_dataset, false_positive_count,true_positive_count,deviations = test(network,num_test_batches,test_batch_size,cutoffs[i],True)
        print("fpc = {}, tpc = {}".format(false_positive_count,true_positive_count))
        print("DEVIATIONS {}".format(deviations))
        print("contaminated {} times, missed {} times, hit {} times".format(num_times_signal_was_contaminated,num_times_signal_was_missed, hits))
        print(num_times_signal_appears_in_dataset)
        false_positives.append(false_positive_count)
        true_positives.append(true_positive_count)
    print(false_positives)
    print(true_positives)

    false_positives_scaled = []
    true_positives_scaled = []
    for i in range(len(false_positives)):
        false_positives_scaled.append(false_positives[i]/(10000-num_times_signal_appears_in_dataset))

    for i in range(len(true_positives)):
        true_positives_scaled.append(true_positives[i]/num_times_signal_appears_in_dataset)

    plt.plot(false_positives_scaled,true_positives_scaled)
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    for i in range(0,len(cutoffs)):
        plt.annotate(xy=[false_positives_scaled[i],true_positives_scaled[i]], s=cutoffs[i])
    plt.savefig(filepath)
    return



cutoffs = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

network = load_network()

make_roc_curve(cutoffs,network,"/Users/mayabasu/PycharmProjects/MNIST-test-neural-net2/matplotlib_output/plot2.png")


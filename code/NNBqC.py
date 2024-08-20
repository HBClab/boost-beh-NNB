# run Quality Check against new sub data

import os
import sys
import pandas as pd

def parse_cmd_args():
    import argparse
    parser = argparse.ArgumentParser(description='QC for ATS')
    parser.add_argument('-s', type=str, help='Path to submission')
    parser.add_argument('-o', type=str, help='Path to output for QC plots and Logs')
    parser.add_argument('-sub', type=str, help='Subject ID')

    return parser.parse_args()

def df(submission):
    submission = pd.read_csv(submission)
    return submission

def qc(submission):
    # convert submission to DataFrame
    submission = df(submission)
     # check if submission is a DataFrame
    if not isinstance(submission, pd.DataFrame):
        raise ValueError('Submission is not a DataFrame. Could not run QC')
    # check if submission is empty
    if submission.empty:
        raise ValueError('Submission is empty')
    # check if submission has correct number of rows (within 5% of expected = 203)
    if len(submission) < 193 or len(submission) > 213:
        raise ValueError('Submission has incorrect number of rows')
    
def plots(submission, output, sub):
    import pandas as pd 
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    df = pd.read_csv(submission)
    test = df[df['block'] == 'test']

    grouped = test.groupby('condition')

    acc_sum = grouped['correct'].sum()
    acc_len = grouped['correct'].count()
    acc = acc_sum / acc_len
    acc = acc.reset_index()
    acc.columns = ['condition', 'accuracy']
    sns.barplot(x='condition', y='accuracy', data=acc)
    plt.title('Accuracy by Condition')
    plt.text(0, 0.6, 'Chance', fontsize=12)
    plt.axhline(0.5, color='black', linestyle='--')
    plt.savefig(os.path.join(output, f'{sub}_ATS_acc.png'))
    plt.close()

    #plot response_time as a scatterplot with transparent box and whiskers
    #create a scatterplot of response_time by condition and create transparent box and whiskers, use transparency to show density, add color coding to show accuracy
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='condition', y='response_time', data=test, showfliers=False, palette='viridis', linewidth=1)
    sns.stripplot(x='condition', y='response_time', data=test, jitter=True, color='black', alpha=0.5, hue='correct')
    sns.despine()
    plt.title('Response time by condition', fontsize=15, pad=20)


    plt.savefig(os.path.join(output, f'{sub}_ATS_rt.png'))
    plt.close()

def main():

    #parse command line arguments
    args = parse_cmd_args()
    submission = args.s
    output = args.o
    sub = args.sub

    # check if submission is a csv
    if not submission.endswith('.csv'):
        raise ValueError('Submission is not a csv')
    # check if submission exists
    if not os.path.exists(submission):
        raise ValueError('Submission does not exist')
    # run QC
    qc(submission)
    
    print(f'QC passed for {submission}, generating plots...')
    # generate plots
    plots(submission, output, sub)
    return submission
    
    
if __name__ == '__main__':
    main()

    
    
    



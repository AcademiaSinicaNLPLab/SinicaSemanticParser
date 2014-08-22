## Edited by MaxisKao @ 2014.08.22
def build(sent, tofile=True):

    """
    sent: input sentence
    tofile: *True/False

    ## input:
    ##  from user:
    ##      sent
    ##  from Server
    ##      ../temp/classifier-output.txt
    ##      ../temp/identifier-output.txt
    ## output: write-to-file or return
    ##  file:
    ##      ../output/output.txt
    """
    arg_list2 = []
    #print sent
    concepts = open('../temp/classifier-output.txt').readlines()
    identifications = open('../temp/identifier-output.txt').readlines()

    for (ident,conc) in zip(identifications, concepts):
        if ident.split(' ')[0] == 'yes':
            arg_str = conc.split(' ')[1]
            pred_lemma = conc.split(' ')[0]
            label = conc.split(' ')[2]
            flat_arg_str_list = arg_str.split('and')
            flat_arg_str_list.append(arg_str)
            for flat_arg in flat_arg_str_list: 
                flat_arg_str = flat_arg.rstrip(' ').lstrip(' ').replace(' ','_').rstrip('_').lstrip('_')
                if label.rstrip() == 'ARG0':
                    arg_list2.append(flat_arg_str+'_'+pred_lemma)
                    #arg_list2.append(flat_arg_str)
                
                else:
                    arg_list2.append(pred_lemma+'_'+flat_arg_str)
                    arg_list2.append(flat_arg_str)
    
    uniq_concepts = list(set(arg_list2)) 

    if tofile:
        ## emit results
        ## using files
        output = open('../output/output.txt','a')
        output.write('<sentence xmlns=\"http://sentic.net/challenge/\" rdf:resource=\"http://sentic.net/challenge/sentence\">'+'\n');
        output.write('<text xmlns=\"http://sentic.net/challenge/\" rdf:datatype=\"http://www.w3.org/TR/rdf-text/\">'+'\n')
        output.write(sent+'\n')
        output.write('</text>\n')
        for concept in uniq_concepts:
            print concept
            output.write('<semantics xmlns="http://sentic.net/challenge/" rdf:resource="http://sentic.net/api/en/concept/'+concept+'"/>'+'\n')
        output.write('</sentence>'+'\n')
        return True
    else:
        ## just return
        return uniq_concepts
  
def my_flatten(node,flat_list):
    if node.data != None and node.data not in ['IN','TO'] and node.word != None and node.word != []:
        flat_list.append(node.word)
    for ch in node.children:
        my_flatten(ch,flat_list)
    return flat_list
                    
if __name__ == "__main__":
 import sys
 try:
    #tree_head_dict = build_tree_head_dict()

    # ----VVVV---- Andy Lee add 20140522
    # input = open('../temp/sent-output.txt')
    # input_sent = input.readlines()
    # sent = ' '.join([l.rstrip().lstrip().rstrip(' ').lstrip(' ')  for l in input_sent])
    # ----^^^^---- Andy Lee add 20140522

    sent = ' '.join(sys.argv[1:])
    build(sent)

 except:
    print >>sys.stderr, __doc__
    raise

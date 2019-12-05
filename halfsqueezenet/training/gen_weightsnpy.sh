#python ./halfsqueezenet_objdetect.py 2  \
#--meta ./train_log/halfsqueezenet_objdetect/NAME1.meta   \
#--model ./train_log/halfsqueezenet_objdetect/NAME2.data-00000-of-00001  \
#--output weights.npy
python ./halfsqueezenet_objdetect.py 2  \
--meta ./train_log/halfsqueezenet_objdetect/graph-1112-161026.meta   \
--model ./train_log/halfsqueezenet_objdetect/model-44530.data-00000-of-00001  \
--output weights.npy
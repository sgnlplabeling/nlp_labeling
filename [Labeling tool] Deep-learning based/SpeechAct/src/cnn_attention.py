import tensorflow as tf


def cnn_attention(inputs, attention_size, pre_y, time_major=False, return_alphas=False):
    ###################################################################
    # 		                                                          #
    #       This attention is a module that calculates the similarity #
    #       between the input sentence and the previous speech act    #
    #                                                                 #
    #       ARG : inputs, attention_size, pre_y         			  #
    # 			                                      				  #
    # 		RETURN : output, alphas(option)         				  #
    # 			    (the attention output of input sentences)  		  #
    # 				                                				  #
    ###################################################################
    if time_major:
        # (T,B,D) => (B,T,D)
        inputs = tf.transpose(inputs, [1, 0, 2])
    hidden_size = 100  # D value - hidden size of the RNN layer

    # Trainable parameters
    w_omega = tf.Variable(tf.random_normal([inputs.shape[2].value, hidden_size], stddev=0.1))
    w_omega2 = tf.Variable(tf.random_normal([pre_y.shape[2].value, hidden_size], stddev=0.1))

    b_omega = tf.Variable(tf.random_normal([hidden_size], stddev=0.1))
    u_omega = tf.Variable(tf.random_normal([hidden_size], stddev=0.1))

    with tf.name_scope('v'):
        v = tf.tanh(tf.tensordot(pre_y, w_omega2, axes=1)  + tf.tensordot(inputs, w_omega, axes=1)  +b_omega) ##best acc

    vu = tf.tensordot(v, u_omega, axes=1)
    alphas = tf.nn.softmax(vu, name='alphas')  # (B,T,A) shape
    output = inputs * tf.expand_dims(alphas, -1)

    if not return_alphas:
        return output
    else:
        return output, alphas
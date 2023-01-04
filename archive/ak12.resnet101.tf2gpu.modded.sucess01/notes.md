# Notes

1. model.keras_model.fit_gen()
2. model here is keras
3. model is set to all the callbacks

    ```[python]
    _callbacks
    [<keras.callbacks.cal...A03506148>, <keras.callbacks.cal...A03506208>, <keras.callbacks.ten...9F37FEA88>, <keras.callbacks.cal...9F37FE808>, <keras.callbacks.cal...9FCF814C8>]
    special variables:
    function variables:
    0: <keras.callbacks.callbacks.BaseLogger object at 0x0000017A03506148>
    1: <keras.callbacks.callbacks.ProgbarLogger object at 0x0000017A03506208>
    2: <keras.callbacks.tensorboard_v2.TensorBoard object at 0x00000179F37FEA88>
    3: <keras.callbacks.callbacks.ModelCheckpoint object at 0x00000179F37FE808>
    4: <keras.callbacks.callbacks.History object at 0x00000179FCF814C8>
    len(): 5
    ```

4. Serialization error on the keras model when setting for callback Tensorboard
5. .to_json error
   - model.to_json
     - model_config = self.updated_config()
       - config = self.get_config()
         - deepcopy(config)
         - More detail about config and specific key that error happened:
           - config: (['name', 'layers', 'input_layers', 'output_layers'])
           - layers: array of item (407 items)
             - ex: `000: {'name': 'input_image', 'class_name': 'InputLayer', 'config': {'batch_input_shape': (...), 'dtype': 'float32', 'sparse': False, 'name': 'input_image'}, 'inbound_nodes': []}`
           - one specific layer (**index 366**) **DETAIL BELOW**


- Detail

    ```[python]
        a
        {'name': 'lambda_1', 'class_name': 'Lambda', 'config': {'name': 'lambda_1', 'trainable': True, 'dtype': 'float32', 'function': (...), 'function_type': 'lambda', 'output_shape': None, 'output_shape_type': 'raw', 'arguments': {}}, 'inbound_nodes': [[...]]}
        special variables:
        function variables:
        'name': 'lambda_1'
        'class_name': 'Lambda'
        'config': {'name': 'lambda_1', 'trainable': True, 'dtype': 'float32', 'function': ('4wEAAAAAAAAAAQAAAAUA...AAAC\nAQ==\n', None, (...)), 'function_type': 'lambda', 'output_shape': None, 'output_shape_type': 'raw', 'arguments': {}}
        'inbound_nodes': [[[...]]]
        special variables:
        function variables:
        0: [['input_gt_boxes', 0, 0, {}]]
        len(): 1
        len(): 4
    ```

- config
- function
- ('4wEAAAAAAAAAAQAAAAUA...AAAC\nAQ==\n', None, (<tf.Tensor 'input_im...e=float32>,))
- (<tf.Tensor 'input_im...e=float32>,)
- Inside
- Use <built-in method **reduce_ex** of Tensor object at 0x000001789AA0C888> to reduce object or sth
- and keep copying

```[python]
{'_op': <tf.Operation 'input...aceholder>, '_value_index': 0, '_dtype': tf.float32, '_tf_output': <tensorflow.python.p...A5ECF30> >, '_shape_val': TensorShape([None, N... None, 3]), '_consumers': [], '_id': 2, '_name': 'input_image:0', '_keras_shape': (None, None, None, 3), '_uses_learning_phase': False, '_keras_history': (<keras.engine.input_...89A78B488>, 0, 0)}
```

- <tf.Operation 'input_image' type=Placeholder>
- inside

    ```[python]
    {'_graph': <tensorflow.python.f...89A9FC608>, '_inputs_val': <tensorflow.python.f...89A74E948>, '_id_value': 1, '_original_op': None, '_traceback': [(...), (...), (...), (...), (...), (...), (...), (...), (...), ...], '_device_code_locations': [], '_colocation_code_locations': {}, '_control_flow_context': None, '_c_op': <Swig Object of type...89A980CC0>, '_is_stateful': False, '_outputs': [<tf.Tensor 'input_im...e=float32>]}
    ```

- <tensorflow.python.framework.func_graph.FuncGraph object at 0x000001789A9FC608>
- inside

```[python]
{'_lock': <unlocked _thread.RL...89A625690>, '_group_lock': <tensorflow.python.u...89A6FEFC8>, '_nodes_by_id': {1: <tf.Operation 'input...aceholder>, 2: <tf.Operation 'input...aceholder>, 3: <tf.Operation 'input...aceholder>, 4: <tf.Operation 'input...aceholder>, 5: <tf.Operation 'input...aceholder>, 6: <tf.Operation 'input...aceholder>, 7: <tf.Operation 'lambd...ype=Shape>, 8: <tf.Operation 'lambd...ype=Const>, 9: <tf.Operation 'lambd...ype=Const>, ...}, '_next_id_counter': 8620, '_nodes_by_name': {'input_image': <tf.Operation 'input...aceholder>, 'input_image_meta': <tf.Operation 'input...aceholder>, 'input_rpn_match': <tf.Operation 'input...aceholder>, 'input_rpn_bbox': <tf.Operation 'input...aceholder>, 'input_gt_class_ids': <tf.Operation 'input...aceholder>, 'input_gt_boxes': <tf.Operation 'input...aceholder>, 'lambda_1/Shape': <tf.Operation 'lambd...ype=Shape>, 'lambda_1/strided_slice/stack': <tf.Operation 'lambd...ype=Const>, 'lambda_1/strided_slice/stack_1': <tf.Operation 'lambd...ype=Const>, ...}, '_version': 8620, '_names_in_use': {'input_image': 1, 'input_image_meta': 1, 'input_rpn_match': 1, 'input_rpn_bbox': 1, 'input_gt_class_ids': 1, 'input_gt_boxes': 1, 'lambda_1': 1, 'lambda_1/shape': 2, 'lambda_1/strided_slice': 2, ...}, '_stack_state_is_thread_local': True, '_thread_local': <_thread._local obje...89A9F8E28>, '_graph_device_function_stack': <tensorflow.python.f...89A799708>, '_default_original_op': None, '_control_flow_context': None, '_graph_control_depen...cies_stack': [], '_collections': {'variables': [...], 'local_variables': [...], 'trainable_variables': [...], (...): [...], (...): [...]}, ...}
```

- Inside
- '_lock' (<unlocked _thread.RLock object owner=0 count=0 at 0x000001789A625690>)
- Dead `TypeError: can't pickle _thread.RLock objects`

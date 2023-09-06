# MMBench Evaluation

## Data

```bash
/cpfs01/shared/public/shusheng.yss/workspace/23082502_qwenvl_eval_test/eval_mm/data/mmbench
```

## Dev

```bash
checkpoint=/PATH/TO/CHECKPOINT
ds=mmbench_dev_20230712
python -m torch.distributed.launch --use-env \
    --nproc_per_node ${NPROC_PER_NODE:-8} \
    --nnodes ${WORLD_SIZE:-1} \
    --node_rank ${RANK:-0} \
    --master_addr ${MASTER_ADDR:-127.0.0.1} \
    --master_port ${MASTER_PORT:-12345} \
    evaluate_multiple_choice_mmbench.py \
    --checkpoint $checkpoint \
    --dataset $ds \
    --batch-size 2 \
    --num-workers 2

# the results will be saved to mmbench_dev_20230712.json

# without consistency constrain

python mmbench_evaluation.py

# with consistency constrain

python mmbench_evaluation_tricky.py

```

## Test

```bash
checkpoint=/PATH/TO/CHECKPOINT
ds=mmbench_test_20230712
python -m torch.distributed.launch --use-env \
    --nproc_per_node ${NPROC_PER_NODE:-8} \
    --nnodes ${WORLD_SIZE:-1} \
    --node_rank ${RANK:-0} \
    --master_addr ${MASTER_ADDR:-127.0.0.1} \
    --master_port ${MASTER_PORT:-12345} \
    evaluate_multiple_choice_mmbench.py \
    --checkpoint $checkpoint \
    --dataset $ds \
    --batch-size 2 \
    --num-workers 2

# the results will be saved to mmbench_test_20230712.json

# convert to submission format with consistency constrain

python mmbench_predict_to_submission.py

```

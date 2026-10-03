import os, torch, torch.distributed as dist

def main():
    if not torch.cuda.is_available():
        raise SystemExit("CUDA GPUs required")
    dist.init_process_group("nccl")
    rank=dist.get_rank(); world=dist.get_world_size()
    local_rank=int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)
    x=torch.tensor([float(rank+1)],device=f"cuda:{local_rank}")
    dist.all_reduce(x,op=dist.ReduceOp.SUM)
    expected=world*(world+1)/2
    print({"rank":rank,"world":world,"value":x.item(),"expected":expected})
    assert x.item()==expected
    dist.destroy_process_group()

if __name__=="__main__": main()

# Run on one multi-GPU node:
# torchrun --standalone --nproc_per_node=2 examples/nccl_all_reduce.py
# Then profile NCCL traffic and compare topology/interconnect.

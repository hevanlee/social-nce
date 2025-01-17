import torch

class MultiAgentTransform():

    def __init__(self, num_human, state_dim=4):
        self.num_human = num_human
        self.mask = torch.ones(num_human, num_human, state_dim).bool()
        for k in range(num_human): self.mask[k, k] = False      

    def transform_frame(self, frame):
        # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        bs = frame.shape[0]
        compare = frame.unsqueeze(1) - frame.unsqueeze(2)                  # [length, num_human, num_human, state_dim]
        compare.to(device='cuda')
        relative = torch.masked_select(compare, self.mask.repeat(bs, 1, 1, 1).to(device='cuda')).reshape(bs, self.num_human, -1)   # [length, num_human, (num_human-1) * state_dim]
        state = torch.cat([frame, relative], axis=2)
        return state

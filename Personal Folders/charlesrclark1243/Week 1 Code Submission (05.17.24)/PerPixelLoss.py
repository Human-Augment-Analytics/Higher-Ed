import torch
import torch.nn as nn

class PerPixelLoss(nn.Module):
    def __init__(self, type: str, size_average=None, reduce=None, reduction='mean'):
        super(PerPixelLoss, self).__init__()

        if type not in ['mse', 'l1']:
            print(f'Invalid input for type parameter, automatically defaulted to MSE\n')
            type = 'mse'

        self.criterion = nn.MSELoss(size_average=size_average, reduce=reduce, reduction=reduction) if type == 'mse' \
            else nn.L1Loss(size_average=size_average, reduce=reduce, reduction=reduction)
        
    def forward(self, out: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        return self.criterion(out, target)
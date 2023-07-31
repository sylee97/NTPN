# nuScenes dev-kit.
# Code written by Freddy Boulton 2020.
from typing import Tuple


import torch
from torch import nn
from torchvision.models import (mobilenet_v2, resnet18, resnet34, resnet50,
                                resnet101, resnet152, resnext50_32x4d, resnext101_32x8d, 
                                wide_resnet50_2, wide_resnet101_2,
                                densenet161)




def trim_network_at_index(network: nn.Module, index: int = -1) -> nn.Module:
    """
    Returns a new network with all layers up to index from the back.
    :param network: Module to trim.
    :param index: Where to trim the network. Counted from the last layer.
    """
    assert index < 0, f"Param index must be negative. Received {index}."
    return nn.Sequential(*list(network.children())[:index])




def calculate_backbone_feature_dim(backbone, input_shape: Tuple[int, int, int]) -> int:
    """ Helper to calculate the shape of the fully-connected regression layer. """
    tensor = torch.ones(1, *input_shape)
    output_feat = backbone.forward(tensor)
    return output_feat.shape[-1]




RESNET_VERSION_TO_MODEL = {'resnet18': resnet18, 'resnet34': resnet34,
                           'resnet50': resnet50, 'resnet101': resnet101,
                           'resnet152': resnet152, 'resnext50_32x4d' : resnext50_32x4d}


RESNEXT_VERSION_TO_MODEL = {'resnext50_32x4d' : resnext50_32x4d, 'resnext101_32x8d' : resnext101_32x8d}


WIDE_RESNET_VERSION_TO_MODEL = {'wide_resnet50_2' : wide_resnet50_2, 'wide_resnet101_2' : wide_resnet101_2}

DENSENET_VERSION_TO_MODEL = { 'densenet161': densenet161}
# 기존 코드
#RESNET_VERSION_TO_MODEL = {'resnet18': resnet18, 'resnet34': resnet34,
#                           'resnet50': resnet50, 'resnet101': resnet101,
#                           'resnet152': resnet152}




class ResNetBackbone(nn.Module):
    """
    Outputs tensor after last convolution before the fully connected layer.


    Allowed versions: resnet18, resnet34, resnet50, resnet101, resnet152.
    """


    def __init__(self, version: str):
        """
        Inits ResNetBackbone
        :param version: resnet version to use.
        """
        super().__init__()


        if version not in RESNET_VERSION_TO_MODEL:
            raise ValueError(f'Parameter version must be one of {list(RESNET_VERSION_TO_MODEL.keys())}'
                             f'. Received {version}.')


        self.backbone = trim_network_at_index(RESNET_VERSION_TO_MODEL[version](), -1)


    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Outputs features after last convolution.
        :param input_tensor:  Shape [batch_size, n_channels, length, width].
        :return: Tensor of shape [batch_size, n_convolution_filters]. For resnet50,
            the shape is [batch_size, 2048].
        """
        backbone_features = self.backbone(input_tensor)
        return torch.flatten(backbone_features, start_dim=1)




class MobileNetBackbone(nn.Module):
    """
    Outputs tensor after last convolution before the fully connected layer.


    Allowed versions: mobilenet_v2.
    """


    def __init__(self, version: str):
        """
        Inits MobileNetBackbone.
        :param version: mobilenet version to use.
        """
        super().__init__()


        if version != 'mobilenet_v2':
            raise NotImplementedError(f'Only mobilenet_v2 has been implemented. Received {version}.')


        self.backbone = trim_network_at_index(mobilenet_v2(), -1)


    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Outputs features after last convolution.
        :param input_tensor:  Shape [batch_size, n_channels, length, width].
        :return: Tensor of shape [batch_size, n_convolution_filters]. For mobilenet_v2,
            the shape is [batch_size, 1280].
        """
        backbone_features = self.backbone(input_tensor)
        return backbone_features.mean([2, 3])


class ResNeXtBackbone(nn.Module):
    """
    Outputs tensor after last convolution before the fully connected layer.


    Allowed versions: resnext50_32x4d, resnext101_32x8d
    """


    def __init__(self, version: str):
        """
        Inits ResNeXtBackbone
        :param version: resnext version to use.
        """
        super().__init__()


        if version not in RESNEXT_VERSION_TO_MODEL:
            raise ValueError(f'Parameter version must be one of {list(RESNEXT_VERSION_TO_MODEL.keys())}'
                             f'. Received {version}.')


        self.backbone = trim_network_at_index(RESNEXT_VERSION_TO_MODEL[version](), -1)


    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Outputs features after last convolution.
        :param input_tensor:  Shape [batch_size, n_channels, length, width].
        :return: Tensor of shape [batch_size, n_convolution_filters]. For resnet50,
            the shape is [batch_size, 2048].
        """
        backbone_features = self.backbone(input_tensor)
        return torch.flatten(backbone_features, start_dim=1)


#        return torch.flatten(backbone_features, start_dim=1)


class WideResNetBackbone(nn.Module):
    """
    Outputs tensor after last convolution before the fully connected layer.


    Allowed versions: wide_resnet50_2, wide_resnet101_2
    """


    def __init__(self, version: str):
        """
        Inits WideResNetBackbone
        :param version: Wideresnet version to use.
        """
        super().__init__()


        if version not in WIDE_RESNET_VERSION_TO_MODEL:
            raise ValueError(f'Parameter version must be one of {list(WIDE_RESNET_VERSION_TO_MODEL.keys())}'
                             f'. Received {version}.')


        self.backbone = trim_network_at_index(WIDE_RESNET_VERSION_TO_MODEL[version](), -1)


    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Outputs features after last convolution.
        :param input_tensor:  Shape [batch_size, n_channels, length, width].
        :return: Tensor of shape [batch_size, n_convolution_filters]. For resnet50,
            the shape is [batch_size, 2048].
        """
        backbone_features = self.backbone(input_tensor)
        return torch.flatten(backbone_features, start_dim=1)


class DenseNetBackbone(nn.Module):
    """
    Outputs tensor after last convolution before the fully connected layer.


    Allowed versions: densenet161
    """


    def __init__(self, version: str):
        """
        Inits DenseNetBackbone
        :param version: Densenet version to use.
        """
        super().__init__()


        if version not in DENSENET_VERSION_TO_MODEL:
            raise ValueError(f'Parameter version must be one of {list(DENSENET_VERSION_TO_MODEL.keys())}'
                             f'. Received {version}.')


        self.backbone = trim_network_at_index(DENSENET_VERSION_TO_MODEL[version](), -1)


    def forward(self, input_tensor: torch.Tensor) -> torch.Tensor:
        """
        Outputs features after last convolution.
        :param input_tensor:  Shape [batch_size, n_channels, length, width].
        :return: Tensor of shape [batch_size, n_convolution_filters]. For resnet50,
            the shape is [batch_size, 2048].
        """
        backbone_features = self.backbone(input_tensor)
        return torch.flatten(backbone_features, start_dim=1)



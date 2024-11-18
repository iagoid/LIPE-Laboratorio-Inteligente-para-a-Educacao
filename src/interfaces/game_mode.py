#!/usr/bin/env python
# coding: utf-8

from abc import ABC, abstractmethod

class IGameMode(ABC):
    @property
    @abstractmethod
    def mode(self) -> int:
        pass
    
    @abstractmethod
    def reset_variables_mode(self):
        pass
        
    @abstractmethod
    def start(self, width: int, height: int):
        pass
            
   
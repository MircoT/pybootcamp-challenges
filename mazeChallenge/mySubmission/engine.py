# -*- coding: utf-8 -*-
"""
The Maze Challenge - Utilities for execute or kill MazeEngine process
Author: prushh
"""
import psutil
import subprocess
from os import path


def _get_process_id(p_name: str) -> int:
    '''
    Check if a process with the same name 'p_name'
    it is running and returns its pid.
    '''
    for proc in psutil.process_iter():
        try:
            if p_name.lower() in proc.name().lower():
                return proc.pid
        except psutil.ZombieProcess:
            pass
        except psutil.NoSuchProcess:
            pass
        except psutil.AccessDenied:
            pass
    return -1


def execute(file_path: str) -> int:
    '''
    Check if 'file_path' exists and it is an executable,
    if it is not running it is started. Returns the process id.
    '''
    if path.exists(file_path):
        p_name, ext = path.splitext(path.basename(file_path))
        if ext in [".exe", ".run"]:
            pid = _get_process_id(p_name)
            if pid == -1:
                try:
                    mazeEngine = subprocess.Popen(file_path)
                    return mazeEngine.pid
                except OSError:
                    print("ERROR: not a valid application for this OS...")
                    return -1
            return pid
        raise Exception("ERROR: unexpected file...")
    raise Exception(f"ERROR: the {file_path} file does not exist...")


def kill(pid: int):
    '''
    Kill process with same pid.
    '''
    try:
        psutil.Process(pid).kill()
    except psutil.ZombieProcess:
        pass
    except psutil.NoSuchProcess:
        pass
    except psutil.AccessDenied:
        pass

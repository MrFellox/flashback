from tkinter import Image
from moviepy.editor import * 
from rich.console import Console
from rich.prompt import Prompt, FloatPrompt, Confirm
from pathlib import Path
from typing import List
import os

try:
    console = Console()
    images: List[ImageClip] = []

    input_path = Prompt.ask('[bold]Enter the path to your pictures folder')
    path = Path(input_path)

    if not path.exists():
        console.print('[bold red]Please specify a valid path.')
        exit(1)

    confirm_path = Confirm.ask(f'[bold]Is [cyan]{str(path.resolve())}[/cyan] the correct path?')

    if not confirm_path:
        console.rule('[bold]Please try again, then.')
        exit(1)

    duration = FloatPrompt.ask('[bold]Enter the duration in seconds for every image in the clip')

    with console.status('Reading images...'):
        for filename in os.listdir(str(path.resolve())):
            if filename.endswith(('.mov', '.mp4', '.mp3', '.heic')):
                continue

            img = ImageClip(os.path.join(str(path.resolve()), filename), duration = duration)
            images.append(img)
        
        console.print(f'[bold green]Found {len(images)} images!')

    output_filename = Prompt.ask('[bold]Enter the name for your video (without the .mp4 extension)', default='output')
    output_filename += '.mp4'

    clip = concatenate_videoclips(images, method='compose')
    save_cur_dir = Confirm.ask('[bold yellow]Save the clip in the current directory?')

    out = None
    if not save_cur_dir:
        output_path = Prompt.ask('[bold]Enter the output path')
        out = Path(output_path)

        if not out.exists():
            console.print('[bold red]Please specify a valid path.')
            exit(1)

    else:
        out = Path(os.getcwd())

    clip.write_videofile(os.path.join(str(out.resolve()), output_filename), fps = 30, threads = 4)
    os.startfile(os.path.join(str(out.resolve()), output_filename))

    exit(0)        
except Exception:
    console.print_exception()
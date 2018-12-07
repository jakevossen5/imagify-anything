# imagify-anything

Backups are hard, what if there was a cheaper, easier way? That would be
awesome, but today, I can show you a cheaper, but much harder way. That being
said, I do not condone breaking any TOS, and am not responsible for any problems
that are caused through the usage of this script. 

With this script, you can turn a zip file (or any other file) into a series of
low resolution images that you can store in other locations. This was a project
for my computer science 101 class, so this is no longer under active
development, but I am still open to pull requests and collaboration to make this
better, as there are a lot of little things that can be improved

## Usage

### Dependencies

First, install the nessesary dependencies with `pip`

```Bash
pip3 install text_to_image
pip3 install progressbar
```

### Downloading

Download `zip2pic.py` either through git clone or directly from GitHub.   

### Running

1. Create a file named `Archive.zip` in the same directory as the script (this
   should be a new directory with nothing else in it)
2. Run `python3 zip2pic.py`. This will create an image directory and fill it
   with all of the images that represent the file. It then double checks it's
   work by creating `final.zip` from the pictures, which should be identical to
   the `Archive.zip` you started with. 
3. When you want to convert back to the file, get all of the files in a
   directory named `images`, and the files must be kept in order via the file
   name. Then run just `convert_from_pictures(img_dir)` with your image
   directory name.

## Notes
You can change the name from `Archive.zip` to any file you want (I think it has
to be a zip file though) by editing the source code near the bottom. 

## TODOs

* Accept file input path through args
* Just create / just convert images through args
* Multi-core generation of images and files

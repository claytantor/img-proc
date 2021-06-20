# %%
import torch
# let's plot these images using torchvision and matplotlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torchvision
import uuid
from cutils import find_files

from imgxform import scale_image_sk
from imgfilter import filter_image
from imgcolorize import get_xml, get_random_pallet, colorize_image

use_gpu = True if torch.cuda.is_available() else False

# trained on high-quality celebrity faces "celebA" dataset
# this model outputs 512 x 512 pixel images
model = torch.hub.load('facebookresearch/pytorch_GAN_zoo:hub',
                       'PGAN', model_name='celebAHQ-512',
                       pretrained=True, useGPU=use_gpu)

def generate_face_gan(out_dir):
    num_images = 1
    noise, _ = model.buildNoiseData(num_images)
    with torch.no_grad():
        generated_images = model.test(noise)

    grid = torchvision.utils.make_grid(generated_images.clamp(min=-1, max=1), scale_each=True, normalize=True)
    plt.axis('off')
    plt.imshow(grid.permute(1, 2, 0).cpu().numpy())
    i_id = str(uuid.uuid4()).replace("-","")[:8]
    filename_gan = '{}/{}.png'.format(out_dir, i_id)
    plt.margins(0.015, tight=True)
    plt.savefig(filename_gan, bbox_inches='tight', pad_inches=0, edgecolor='w')
    return filename_gan




# %%
def pipeline():
    filename_gan = generate_face_gan("workspace/ghosts_gan/gengan")
    filename_gan_s = scale_image_sk(filename_gan, "workspace/ghosts_gan/gengan_s", float(2.775067751) )
    filename_gan_g = filter_image(filename_gan_s,  "workspace/ghosts_gan/gengan_g", filter="rgb2grey")
    filename_gan_g_rgb = filter_image(filename_gan_g,  "workspace/ghosts_gan/gengan_g_rgb", filter="grey2rgb")
    colors = get_xml("workspace/ghosts_gan/colors.xml")
    img_model = colorize_image(filename_gan_g_rgb, "workspace/ghosts_gan/gengan_g_color", get_random_pallet(colors))
    # print(img_model)
    filename_gan_rgb_c = filter_image(img_model['out_img'],  "workspace/ghosts_gan/gengan_rgb_contrast", filter="rescale_intensity")

    return filename_gan_rgb_c
    
# %%
# pipeline()
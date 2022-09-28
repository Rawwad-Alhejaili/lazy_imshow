# lazy_imshow
This repo features a rather convenient imshow function.

I am sure that I speak for everyone when I say that although `matplotlib.pyplot.imshow` brings amazing functionality to python, its defaults leave a LOT to be desired. For example:

- The default DPI is so freaking LOW which causes the output image to have terrible quality.
- The size of the image is so small that even a short title could be wider than the image. This is problematic when you have multiple subplots because their titles will overlap and cause a mess.
- Unless your image has a range from 0 to 1, you will have to manually convert the input image to uint8 so that `plt.imshow` "shows" the right range (by default, the range is from 0 to 1, but for uint8, it is from 0 to 255).
- For God knows why, grayscale image are shown with pseudo-color.
- Using cmap='gray' will show the normailzed image, which can be annoying due to its inconsitency (what was the point behind converting the image to uint8?).
- Images are shown with useless axes.
- Good luck showing an image that resides on the GPU (tensors in general cause a heap of problems).
- Showing images in subplots takes too much soace in the code.

I could go on, but I guess you get the point now. Having to fix all this every single time I use `plt.imshow` gets REALLY annoying very quickly (remember that it is still an amazing fucntion all things considered). As such, I decided to write what I would call a "convenience function", and it is `imshow`. I decided to write this function to cut down on the tedium. Below I will write a summary that includes most of the capabilities provided here.

# Features:
- Accepts multiple images and shows them on a specified grid (e.g. 2x2 vs 1x4).
- Titles can be assigned to multiple images (optional).
- All images are shown in a unified range. Range of the last image is used by default (configurable via the `rang` arguement).
- Adds a colorbar to the right (can be toggled on or off from the arguements).
- Can automatically clip the minimum and maximum `n` percentile of the image (very useful for seismic images).
- Padding between the images is configurable (default = 0.7)
- Automatically applies `cmap='seismic_r'` to one channel images (configurable).
- Removes the axes from the image (will be added in a future release to account for the offset and time axes in seismic images).
- Works with tensors (by moving them to the cpu and detaching the gradients).
- Works with 4D arrays (it uses the first sample for convenience).
- Automatically moves the channel axis position to the last axis.
- Sets the DPI to 300 by default (configurable).
- The figure can be set to be transparent (hope that I spelled that right)
- Other `plt.imshow` arguments can be passed as named arguements `kwargs`.

# Example
Below is a fairly tame example comparing the the usage `plt.imshow` and `imshow`.

Instead of writing:
```
plt.figure(dpi=300, figsize=(5,5))

plt.subplot(2,2,1)
plt.axis('off')
plt.title('Boo!')
plt.imshow(np.uint8(Im1*255), cmap='gray', vmin=0, vmax=255)

plt.subplot(2,2,2)
plt.axis('off')
plt.title('Boo!')
plt.imshow(np.uint8(Im2*255), cmap='gray', vmin=0, vmax=255)

plt.subplot(2,2,3)
plt.axis('off')
plt.title('Boo!')
plt.imshow(np.uint8(Im3*255), cmap='gray', vmin=0, vmax=255)

plt.subplot(2,2,4)
plt.axis('off')
plt.title('Boo!')
plt.imshow(np.uint8(Im4*255), cmap='gray', vmin=0, vmax=255)
```

Now you only to need to type:
```
Im = [Im1, Im2, Im3, Im4]
titles = ['title1', 'title2', 'title3', 'title4']
imshow(Im, titles, cmap='gray', grid=(2,2))
```

And the function will take care of the rest. It can take care of graysacle 2D or 3D images, RGB images, and it also works with tensors (though that's an experimental feature). It can do all that automatically, and it will also adjust the range of the image accordingly.

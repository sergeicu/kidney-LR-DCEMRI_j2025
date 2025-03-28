import numpy as np

"""
DETAILED DESCRIPTION: 
This function accepts k-space data (k_space), star sampling information (k_samples), square root of the density compensation factor (sqrt_dcf), 
and coil profile matrix (coil_p). It optionally downsamples these arrays in the frequency domain by a factor specified in factor. 
If factor is provided, it downsamples k_space, k_samples, and sqrt_dcf accordingly. 
Additionally, it crops the coil_p matrix symmetrically based on the downsampling factor to adjust for the reduced field of view in the image domain. 
The function then returns the modified versions of k_space, k_samples, sqrt_dcf, and coil_p.

"""




def down_sample_freq(k_space: np.ndarray,
                     k_samples: np.ndarray,
                     sqrt_dcf: np.ndarray,
                     coil_p: np.ndarray,
                     factor: int = None):
    """ This function downsamples the frequency components on the input and crops
        image domain data with respect to a predefined factor
        Args:
            k_space(ndarray[complex]): [Nv x NS x NC x NSp] k_space observation
            k_samples(ndarray[float]): [Nv x NS x NSp] star sampling information
            sqrt_dcf(ndarray[complex]): [Nv x NS x NSp] square root of the dcf matrix
            coil_p(ndarray[complex]): [NS x NS x NC] coil profile matrix
                [Nv,NS,NC,NSp] = [num_volume, num_sample, num_coil, num_spoke]
            factor(int): downsampling in frequency domain factor (fov scaling on image)
        Return: Rescaled versions of
            k_space(ndarray[complex]): [Nv x NS x NC x NSp] k_space observation
            k_samples(ndarray[float]): [Nv x NS x NSp] star sampling information
            sqrt_dcf(ndarray[complex]): [Nv x NS x NSp] square root of the dcf matrix
            coil_p(ndarray[complex]): [NS x NS x NC] coil profile matrix """

    if factor:
        k_space = k_space[:, ::factor, :, :]
        k_samples = k_samples[:, ::factor, :]
        sqrt_dcf = sqrt_dcf[:, ::factor, :]
        side_crop = int(coil_p.shape[0] * (1 - (1 / factor)) / 2)
        coil_p = coil_p[
                 side_crop:coil_p.shape[0] - side_crop,
                 side_crop:coil_p.shape[1] - side_crop, :]

    return k_space, k_samples, sqrt_dcf, coil_p

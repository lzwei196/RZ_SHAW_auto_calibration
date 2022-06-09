# Welcome to RZ_SHAW_autocalibration
`RZ_SHAW_autocalibration` is an open source program that offers the user the ability to calibrate the parameters for snow depth and soil temperature. The program emploies the Sobol sequence to sample the value sets based on desired range and numbers for the variables. The result for each run will be recorded in the MySQL database with the NSE and RMSD values, along with the potential errors outputted from the the RZ-SHAW model.  

#update 06/06
`Added support for parallel and distributed computing. The distributed computing is based on ray, parallel computing is based on the multiprocessing module. For detailed usages, contact leo.li@mail.mcgill.ca`

# Pre-requirement
* Python 3.7 or above installed
* PyTorch installed. PyTorch's SOBOL engine:
`https://pytorch.org/docs/stable/generated/torch.quasirandom.SobolEngine.html`
* numPY installed
* Latest version of RZWQM installed
`link: https://www.ars.usda.gov/plains-area/fort-collins-co/center-for-agricultural-resources-research/rangeland-resources-systems-research/docs/system/rzwqm/`
* Created RZWQM scenario for `Guide can be found in the documentation folder of RZWQM`
* Created MySQL database `.DB_fn/DB_structure.py`

## Current parameters availiable for calibration:
* Average maximum snowpack density
* Initial snowpack density (new fallen snow)
* Wet albedo
* Dry albedro
* Ksat
* Bubbling pressure
* Soil composition<br>
More variables can be added upon user selection, with known file path and line number.<br>
`def write_to_file_with_changed_val(path_to_write, data, line_num, changed_line)`

## Usage
To start the auto calibration, users can call the main module `def return sample points`
to generate the matrix for the testing values.<br>
User can then create for loop to go through each set of value calling `write to file with changed val`,
then call ` subprocess.run` to initiate simulation for each run.

Example:
```    
        for count, val in enumerate(avg_snow):#iterating through the sample sets
            obj = {0 : val, 1 : init_snow[count]}
            changing_line = lines[line_n]
            sno_line = rzwqm.change_param_val_in_one_line(obj, changing_line)
            write_to_file_with_changed_sno_val('C:/RZWQM2/lods/Meteorology/new.sno', lines, line_n, sno_line)
            #start the simulation
            subprocess.run('C:/RZWQM2/lods/RZWQMrelease.exe', cwd=r'C:\RZWQM2\lods\lods')
            time.sleep(2)
            t_nse = return_nse()
            t_rmsd = return_rmsd()
            add_snow_test_res(val, init_snow[count], t_nse, t_rmsd)
```

Credit to:
Zhiming Qi Zhiming.qi@McGill.ca
Ziwei Li   Leo.li@mail.mcgill.ca

For further questions,
contact leo.li@mail.mcgill.ca

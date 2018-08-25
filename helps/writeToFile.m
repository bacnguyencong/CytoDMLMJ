function writeToFile(file, conts)
    out = fopen(file,'a');
    fprintf(out,'%s',conts);
    fclose(out);
end
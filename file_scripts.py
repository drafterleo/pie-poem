import os

def merge_txt_files_from_dir(in_dir_name, out_file_name):
    f_out = open(out_file_name, mode='w', encoding='utf-8')
    for file in os.listdir(in_dir_name):
        if file.endswith(".txt"):
            f_in = open(in_dir_name + file, mode='r', encoding='utf-8')
            lines = f_in.readlines()
            for line in lines:
                f_out.write(line)
            f_out.write('\n\n')

def save_poems_to_file(poem_model, file_name):
    f_out = open(file_name, mode='w', encoding='utf-8')
    for poem in poem_model['poems']:
        f_out.write(poem + '\n')


if __name__ == "__main__":
    merge_txt_files_from_dir("C:/temp/poem_base/", "poem_merged.txt")
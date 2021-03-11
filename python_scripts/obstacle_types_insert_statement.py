"""
Get obstacle types from DOF (Digital Obstacle File) and create INSERT INTO statements for
obstacle_type table.
"""
import sys


def get_obstacle_types(dof_path):
    """ Get list of obstacle types.
    :param: dof_path: str, full path to Digital Obstacle File
    :return: obstacle_types: list
    """
    obstacle_type_start = 62
    obstacle_type_end = 81
    line_number = 0
    obstacle_types = []

    with open(dof_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_number += 1
            if line_number >= 5:
                obstacle_type = line[obstacle_type_start:obstacle_type_end].strip()
                if obstacle_type not in obstacle_types:
                    obstacle_types.append(obstacle_type)
    return obstacle_types


def generate_insert_statement(obstacle_types):
    """ Create formatted INSERT INTO statement
    :param: obstacle_types: list
    :return: inert_statement: str
    """
    inert_statement = "INSERT INTO obstacle_type (obst_type)\nVALUES\n"
    obstacle_types.sort()

    for obs_type in obstacle_types[:-1]:
        inert_statement += "\t('{}'),\n".format(obs_type)
    inert_statement += "\t('{}');".format(obstacle_types[-1])
    return inert_statement


def write_insert_statement_to_file(insert_statement, base_name):
    """ Write SQL INSERT INTO statement into file.
    insert_statement: str,
    base_name: str: file name for insert statement without extension, ".sql" extension will be added automatically
    """
    file_name = '{}.sql'.format(base_name)
    with open(file_name + '.sql', 'w') as f:
        for line in insert_statement:
            f.write(line)


def print_help():
    print("Gets obstacle data types and store them into sql file as ready to use INSERT INTO statement.")
    print("Usage:")
    print("obstacle_types_insert_statement.py <DOF_file> <insert_statement_fie>")
    print("<DOF_file>: full path to Digitial Obstacle File, example 'C:\\DOF.DAT'")
    print("<insert_statement_fie>: base nae (without extension) file with INSERT statement, example 'obst_types'")


def generate_obstacle_type_insert_into_statement(dof_path, base_name):
    obstacle_types = get_obstacle_types(dof_path)
    insert_statement = generate_insert_statement(obstacle_types)
    write_insert_statement_to_file(insert_statement, base_name)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_help()
    else:
        dof_path = sys.argv[1]
        base_name = sys.argv[2]
        generate_obstacle_type_insert_into_statement(dof_path, base_name)

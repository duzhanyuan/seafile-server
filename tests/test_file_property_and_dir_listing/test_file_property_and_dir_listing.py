import pytest
from tests.config import USER
from seaserv import seafile_api as api

def test_file_property_and_dir_listing ():

    t_repo_id = None
    t_repo_version = 1
    t_repo_id = api.create_repo('test_file_property_and_dir_listing', '', USER, passwd=None)
    api.post_file(t_repo_id, '/home/ly/test/test.txt', '/', 'test.txt', USER)
    api.post_dir(t_repo_id, '/', 'test_dir', USER)
    api.post_file(t_repo_id, '/home/ly/test/test.txt', '/test_dir', 'test.txt', USER)

    #test is_valid_filename
    t_valid_file_name = 'valid_filename'
    t_invalid_file_name = '/invalid_filename'
    assert api.is_valid_filename(t_repo_id, t_valid_file_name)
    assert api.is_valid_filename(t_repo_id, t_invalid_file_name) == 0

    #test get_file_id_by_path
    t_file_id = None
    t_file_id = api.get_file_id_by_path(t_repo_id, '/test.txt')
    assert t_file_id

    #test get_dir_id_by_path
    t_dir_id = None
    t_dir_id = api.get_dir_id_by_path(t_repo_id, '/test_dir')
    assert t_dir_id

    #test get_file_size
    test_file_size = 18
    assert test_file_size == api.get_file_size(t_repo_id, t_repo_version, t_file_id)

    #test get_dir_size
    test_dir_size = 18
    assert test_dir_size == api.get_dir_size(t_repo_id, t_repo_version, t_dir_id)

    #test get_file_id_by_commit_and_path
    t_repo = None
    t_file_id_tmp = t_file_id
    t_repo = api.get_repo(t_repo_id)
    assert t_repo
    t_commit_id = t_repo.head_cmmt_id
    t_file_id = api.get_file_id_by_commit_and_path(t_repo_id,
                                                   t_commit_id,
                                                   '/test.txt')

    assert t_file_id == t_file_id_tmp

    #test get_dirent_by_path
    std_file_mode = 0100000 | 0644
    t_dirent_obj = api.get_dirent_by_path(t_repo_id, 'test.txt')
    assert t_dirent_obj
    assert t_dirent_obj.obj_id == t_file_id
    assert t_dirent_obj.obj_name == 'test.txt'
    assert t_dirent_obj.mode == std_file_mode
    assert t_dirent_obj.version == t_repo_version
    assert t_dirent_obj.size == test_file_size
    assert t_dirent_obj.modifier == USER

    #test list_file_by_file_id
    t_block_list = None
    t_block_list =  api.list_file_by_file_id(t_repo_id, t_file_id)
    assert t_block_list

    #test list_blocks_by_file_id
    t_block_list = None
    t_block_list = api.list_blocks_by_file_id(t_repo_id, t_file_id)
    assert t_block_list

    #test list_dir_by_dir_id
    t_dir_list = None
    t_dir_list = api.list_dir_by_dir_id(t_repo_id, t_dir_id)
    assert t_dir_list

    #test list_dir_by_path
    t_dir_list = None
    t_dir_list = api.list_dir_by_path(t_repo_id, '/test_dir')
    assert t_dir_list

    #test get_dir_id_by_commit_and_path
    t_dir_id = None
    t_dir_id = api.get_dir_id_by_commit_and_path(t_repo_id, t_commit_id, '/test_dir')
    assert t_dir_id

    #test list_dir_by_commit_and_path
    t_dir_list = None
    t_dir_list = api.list_dir_by_commit_and_path(t_repo_id, t_commit_id, '/test_dir')
    assert t_dir_list

    #test list_dir_with_perm
    t_dir_list = None
    t_dir_list = api.list_dir_with_perm(t_repo_id, '/test_dir', t_dir_id, USER)
    assert t_dir_list

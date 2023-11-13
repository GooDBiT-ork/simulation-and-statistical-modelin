import sys
import zipfile
import win32security

def serialize(input_file, output_file):
  sd = win32security.GetFileSecurity(input_file, win32security.DACL_SECURITY_INFORMATION)
  string_dacl = win32security.ConvertSecurityDescriptorToStringSecurityDescriptor(sd, win32security.SDDL_REVISION_1, win32security.DACL_SECURITY_INFORMATION)
  with zipfile.ZipFile(output_file, 'w') as z:
    z.writestr('perms', string_dacl)

def deserialize(input_file, output_file):
  with zipfile.ZipFile(input_file, 'r') as z:
    string_dacl = z.read('perms')
  sd = win32security.ConvertStringSecurityDescriptorToSecurityDescriptor(string_dacl.decode('utf-8'), win32security.SDDL_REVISION_1)
  dacl = sd.GetSecurityDescriptorDacl()
  with open(output_file, 'wb') as f:
    win32security.SetNamedSecurityInfo(output_file, win32security.SE_FILE_OBJECT, 
                                   win32security.DACL_SECURITY_INFORMATION, 
                                   None, None, dacl, None)

if __name__ == '__main__':
  if sys.argv[1] == '--serialize':
    serialize(sys.argv[3], sys.argv[5])
  elif sys.argv[1] == '--deserialize':
    deserialize(sys.argv[3], sys.argv[5])

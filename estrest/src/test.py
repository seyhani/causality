from helper import Helper

helper = Helper()

a = helper.new_expr("a")

xyz = helper.new_expr("z")
xyz = helper.prefix(xyz, "y")
xyz = helper.prefix(xyz, "x")

helper.product(a, xyz)

helper.export()

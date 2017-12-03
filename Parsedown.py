import re
import sys

class parser:

	name_file = ""
	read_file 	= 0
	current_line 	= 0
	current_row 	= 0
	number_line	= 0
	before_line = 0
	list_block = []
	flag_ident = False
	flag_check_p = False
	flag_lists = False
	flag_enum = False

	def __init__(self, file_name):
		self.read_file= open(file_name, 'r')
		self.name_file = file_name
		self.recognize()
		

	def clear(self, line):
		line = line.replace("\t", "")
		line = line.replace("\n", "")
		return line

	def next_line(self):
		self.before_line = self.current_line
		text = self.read_file.readline()
		if text == "":
			return False
		text = self.clear(text)
		self.current_line = text.strip(" ")
		self.number_line += 1
		self.current_row = 0
		return True

	def check_indent(self):
		if re.match("^([>])", self.current_line):
			if self.flag_ident == False:
				self.flag_ident = True
				self.list_block.append("<blockquote>")
			self.current_line = "	" + re.sub(r"([>])", r"", self.current_line).strip()
		elif self.flag_ident:
			self.flag_ident = False
			self.list_block.append("</blockquote>")

	def replace_line(self, line, index):
		self.list_block[index] = line


	def check_h1(self):
		if (re.match("[=+]" , self.current_line)) and (re.match("[a-zA-Z]+", self.before_line)):
			self.replace_line("<h1>" + self.before_line + "</h1>", len(self.list_block)-1)	
			self.flag_check_p = False
			return True
		return False

	def check_h2(self):
		if re.match("\s*([#]{2})", self.current_line):
			self.current_line = re.sub(r"([#]{2}\s*)", r"<h2>", self.current_line)
			self.list_block.append(self.current_line + "</h2>")
			return True
		elif (re.match("[-+]" , self.current_line)) and (re.match("[a-zA-Z]+", self.before_line)):
			self.replace_line("<h2>" + self.before_line + "</h2>", len(self.list_block)-1)	
			self.flag_check_p = False
			return True
		return False

	def check_h3(self):
		if re.match("^([*#]{3})", self.current_line):
			self.current_line = re.sub(r"(^[#]{3}\s*)", r"<h3>", self.current_line)
			self.list_block.append(self.current_line + "</h3>")
			return True
		return False


	def check_p(self):
		if not self.check_h3() and not self.check_h2() and not self.check_h1() and not self.check_lists() and not self.check_enum():			
			if (len(self.current_line.strip()) > 0):
				var = self.current_line.strip()
				if (self.flag_check_p == False):
					self.flag_check_p = True
					var = "<p>" + var
				if self.flag_ident:
					var = "	" + var
				self.list_block.append(var)
			else:
				self.list_block.append(self.current_line)
				self.close_p()
		else:
			self.close_p()
			

	def close_p(self):
		if self.flag_check_p:
			self.flag_check_p = False
			index = len(self.list_block)-2
			aux = self.list_block[index]
			self.replace_line(aux + "</p>", index)

	def check_lists(self):
		if re.match("^([+*-])", self.current_line):
			if self.flag_lists == False:
				self.flag_lists = True
				self.list_block.append("<ul>")
			self.list_block.append(re.sub(r"(^([+*-]))", r"<li>", self.current_line).strip() + "</li>")
			return True
		elif self.flag_lists:
			self.flag_lists = False
			self.list_block.append("</ul>")
			return True
		return False

	def check_enum(self):
		if re.match("^(\d\.)", self.current_line):
			if self.flag_enum == False:
				self.flag_enum = True
				self.list_block.append("<ol>")
			self.list_block.append(re.sub(r"(^(\d\.))", r"<li>", self.current_line).strip() + "</li>")
			return True
		elif self.flag_enum:
			self.flag_enum = False
			self.list_block.append("</ol>")
			return True
		return False

	def recognize(self):
		while (self.next_line()):				
			self.check_indent()
			self.check_p()
			
		if self.flag_ident:
			self.list_block.append("</blockquote>")

		if self.flag_lists:
			self.list_block.append("</ul>")

		if self.flag_enum:
			self.list_block.append("</ol>")
	
		for x in self.list_block:
			print(x)

if __name__ == "__main__":
	name = sys.argv[1]
	parser(name)


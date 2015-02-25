
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = 'M\xdck\x15\xd8\x7f\x87\x98\x135\x93]Q\xcbQ\\'
    
_lr_action_items = {'RETURN':([0,3,4,10,11,14,29,32,33,],[13,-7,13,13,-8,-9,-19,-10,-11,]),'SEMICOLON':([2,5,7,12,15,17,21,23,26,27,28,30,34,],[-6,-18,-15,-17,-16,29,-21,-14,32,33,-22,-6,-20,]),'ADV_ASSIGNMENT_OP':([2,5,7,12,15,23,],[18,-18,-15,-17,-16,-14,]),'NUMBER':([16,18,20,],[28,-12,-13,]),'BLOCK_BEGIN':([0,],[4,]),'COMMA':([2,5,7,12,15,23,30,],[19,-18,-15,-17,-16,-14,19,]),'PRIVATE':([0,3,4,10,11,14,29,32,33,],[8,-7,8,8,-8,-9,-19,-10,-11,]),'VARIABLE':([0,3,4,8,10,11,13,14,19,29,32,33,],[5,-7,5,5,5,-8,5,-9,5,-19,-10,-11,]),'HASH':([0,3,4,8,10,11,13,14,19,29,32,33,],[12,-7,12,12,12,-8,12,-9,12,-19,-10,-11,]),'ARRAY':([0,3,4,8,10,11,13,14,19,29,32,33,],[15,-7,15,15,15,-8,15,-9,15,-19,-10,-11,]),'ASSIGNMENT_OP':([2,5,7,12,15,23,],[20,-18,-15,-17,-16,-14,]),'BLOCK_ENDS':([3,10,11,14,22,24,25,29,32,33,],[-7,-6,-8,-9,31,-4,-5,-19,-10,-11,]),'$end':([1,3,6,9,10,11,14,24,25,29,31,32,33,],[-2,-7,0,-1,-6,-8,-9,-4,-5,-19,-3,-10,-11,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statements':([0,4,10,],[1,22,24,]),'assignmenttype':([2,],[16,]),'lefthandside':([0,4,10,],[2,2,2,]),'assignment':([0,4,10,],[3,3,3,]),'decList':([2,30,],[17,34,]),'expression':([16,],[27,]),'start':([0,],[6,]),'empty':([2,10,30,],[21,25,21,]),'statement':([0,4,10,],[10,10,10,]),'declaration':([0,4,10,],[11,11,11,]),'returnStatement':([0,4,10,],[14,14,14,]),'type':([0,4,8,10,13,19,],[7,7,23,7,26,30,]),'block':([0,],[9,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> block','start',1,'p_start','parser1.py',17),
  ('start -> statements','start',1,'p_start','parser1.py',18),
  ('block -> BLOCK_BEGIN statements BLOCK_ENDS','block',3,'p_block','parser1.py',21),
  ('statements -> statement statements','statements',2,'p_statments','parser1.py',24),
  ('statements -> statement empty','statements',2,'p_statments','parser1.py',25),
  ('empty -> <empty>','empty',0,'p_empty','parser1.py',27),
  ('statement -> assignment','statement',1,'p_statment','parser1.py',34),
  ('statement -> declaration','statement',1,'p_statment','parser1.py',35),
  ('statement -> returnStatement','statement',1,'p_statment','parser1.py',36),
  ('returnStatement -> RETURN type SEMICOLON','returnStatement',3,'p_returnStatement','parser1.py',55),
  ('assignment -> lefthandside assignmenttype expression SEMICOLON','assignment',4,'p_assignment','parser1.py',59),
  ('assignmenttype -> ADV_ASSIGNMENT_OP','assignmenttype',1,'p_assignmenttype','parser1.py',62),
  ('assignmenttype -> ASSIGNMENT_OP','assignmenttype',1,'p_assignmenttype','parser1.py',63),
  ('lefthandside -> PRIVATE type','lefthandside',2,'p_lefthandside','parser1.py',66),
  ('lefthandside -> type','lefthandside',1,'p_lefthandside','parser1.py',67),
  ('type -> ARRAY','type',1,'p_type','parser1.py',70),
  ('type -> HASH','type',1,'p_type','parser1.py',71),
  ('type -> VARIABLE','type',1,'p_type','parser1.py',72),
  ('declaration -> lefthandside decList SEMICOLON','declaration',3,'p_declaration','parser1.py',76),
  ('decList -> COMMA type decList','decList',3,'p_decList','parser1.py',79),
  ('decList -> empty','decList',1,'p_decList','parser1.py',80),
  ('expression -> NUMBER','expression',1,'p_expression_number','parser1.py',87),
]

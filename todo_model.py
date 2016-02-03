# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    # _parent_name = 'parent_id'
    name = fields.Char('Name')
    parent_id = fields.Many2one('todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)

class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence,name'
    # String fields:
    name = fields.Char('Name')
    desc = fields.Text('Description')
    state = fields.Selection([('draft','New'), ('open','Started'),('done','Closed')],'State')
    docs = fields.Html('Documentation')
    # Numeric fields:
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('%d Complete', (3, 2))
    # Date fields:
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Changed')
    # Other fields:
    fold = fields.Boolean('Folded?')

    image = fields.Binary('Image')
    # Relational fields
    task_ids = fields.One2many("todo.task", "stage_id", string="Tasks")

class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')

    stage_fold = fields.Boolean(
        string='Stage Folded?',
        compute='_compute_stage_fold',
        # store=False) # the default
        search='_search_stage_fold',
        inverse='_write_stage_fold')

    stage_state = fields.Selection(
        related='stage_id.state',
        string='Stage State')

    user_todo_count = fields.Integer('User To-Do Count', compute='compute_user_todo_count')

    stage_fold = fields.Boolean('Folded?', compute='_compute_stage_fold')

    effort_estimate = fields.Integer('Effort Estimate')

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]
    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count([('user_id', '=', self.user_id.id)])

    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

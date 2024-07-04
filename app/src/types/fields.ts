export enum FieldType {
  BOOLEAN = 'boolean',
  CHECKLIST = 'checklist',
  CHOICE = 'choice',
  DATE = 'date',
  FILE = 'file',
  NUMBER = 'number',
  RELATION = 'relation',
  TEXT = 'text'
}

export interface IField {
  id: string
  created_at: string
  updated_at: string
  created_by: string
  updated_by: string

  database: string
  label: string
  field_type: FieldType
  config: any
}

export interface IFieldWithResponse extends IField {
  response: {
    data: any
  }
}

export interface IFieldCreateRequest {
  database: string
  label?: string
  field_type?: FieldType
  config?: any
}

export interface IFieldUpdateRequest {
  id: string
  label?: string
  field_type?: FieldType
  config?: any
}

from Core import Column
from Core import Table
from Core.Granularity import GranularityTemporal
from Core.Enum_Type import Enum_Type
from Source.SourceFile.SourceCSV import SourceCSV



columns = [Column('channel ID',Enum_Type.STRING,None),
          Column('slot',Enum_Type.STRING,None),
          Column('week',Enum_Type.STRING,None),
          Column('genre ID',Enum_Type.STRING,None),
          Column('duration',Enum_Type.STRING,None),
          Column('subGenre ID',Enum_Type.STRING,None),
          Column('user ID',Enum_Type.STRING,None),
          Column('program ID',Enum_Type.STRING,None),
          Column('event ID',Enum_Type.STRING,None)
          ]






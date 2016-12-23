#!/usr/bin/env python3
import os
import peewee
from peewee import CharField, ForeignKeyField

db_file_name = "data.sq3"

database = peewee.SqliteDatabase(db_file_name)

class BaseModel(peewee.Model):
    class Meta:
        database = database

class Airport(BaseModel):
    name = CharField(unique=True)
    icao_code = CharField(unique=True, index=True)
    class Meta:
        order_by = ('icao_code', )

class Pilot(BaseModel):
    first_name = CharField()
    last_name = CharField()
    code = CharField(unique=True)
    class Meta:
        order_by = ('code', )

class ACType(BaseModel):
    name = CharField()
    manufacturer = CharField()
    multi_engine = CharField()
    what_is_it = CharField() # As in plane, heli, glider

class Aircraft(BaseModel):
    actype = ForeignKeyField(ACType, related_name='aircraft')
    registration = CharField(unique=True)
    instrument_capable = CharField()
    class Meta:
        order_by = ('registration', )

class Company(BaseModel):
    name = CharField(unique=True)
    class Meta:
        order_by = ('name', )

class Company(BaseModel):
    name = CharField(unique=True)


if __name__ == "__main__":
    answer = input("Delete database and reinitialize tables? (y/n): ")
    if answer in 'yY':
        os.remove(db_file_name)
        try:
            Airport.create_table()
            Pilot.create_table()
            ACType.create_table()
            Aircraft.create_table()
            Company.create_table()
            # add some data
            pilot_data = [
                {'first_name': 'Radu', 'last_name': 'Ciurlea', 'code': 'CIR'},
                {'first_name': 'Radu', 'last_name': 'Marin', 'code': 'MAL'},
                {'first_name': 'Petre', 'last_name': 'Stroe', 'code': 'STR'},
                {'first_name': 'Gabi', 'last_name': 'Mustaţă', 'code': 'MUS'},
                {'first_name': 'Mihai', 'last_name': 'Asofrone', 'code': 'ASO'},
                {'first_name': 'Eugen', 'last_name': 'Ciocan', 'code': 'CIO'}
            ]

            airport_data = [
                {'name': 'Băneasa', 'icao_code': 'LRBS'},
                {'name': 'Otopeni', 'icao_code': 'LROP'},
                {'name': 'Strejnic', 'icao_code': 'LRPW'},
                {'name': 'Craiova', 'icao_code': 'LRCV'},
                {'name': 'Sibiu', 'icao_code': 'LRSB'},
                {'name': 'Târgu Mureş', 'icao_code': 'LRTM'},
                {'name': 'Timişoara', 'icao_code': 'LRTR'},
                {'name': 'Oradea', 'icao_code': 'LROD'},
                {'name': 'Bacău', 'icao_code': 'LRBC'},
                {'name': 'Iaşi', 'icao_code': 'LRIA'},
                {'name': 'Suceava', 'icao_code': 'LRSV'},
                {'name': 'Constanţa', 'icao_code': 'LRCK'},
                {'name': 'Tuclea', 'icao_code': 'LRTC'}
            ]

            actype_data = [
                {'name': '206', 'manufacturer': 'Bell', 'multi_engine': 'No', 'what_is_it': 'Helicopter'},
                {'name': 'R22', 'manufacturer': 'Robinson', 'multi_engine': 'No', 'what_is_it': 'Helicopter'},
                {'name': 'R44', 'manufacturer': 'Robinson', 'multi_engine': 'No', 'what_is_it': 'Helicopter'},
                {'name': 'EC120', 'manufacturer': 'Airbus Helicopters', 'multi_engine': 'No', 'what_is_it': 'Helicopter'},
                {'name': 'EC155', 'manufacturer': 'Airbus Helicopters', 'multi_engine': 'Yes', 'what_is_it': 'Helicopter'},
                {'name': 'AS355', 'manufacturer': 'Airbus Helicopters', 'multi_engine': 'Yes', 'what_is_it': 'Helicopter'},
                {'name': '172', 'manufacturer': 'Cessna', 'multi_engine': 'No', 'what_is_it': 'Plane'}
            ]

            aircraft_data = [
                {'actype': 1, 'registration': 'YR-OIL', 'instrument_capable': 'No'},
                {'actype': 2, 'registration': 'YR-MDV', 'instrument_capable': 'No'},
                {'actype': 2, 'registration': 'YR-MDX', 'instrument_capable': 'No'},
                {'actype': 4, 'registration': 'YR-MDG', 'instrument_capable': 'No'},
                {'actype': 4, 'registration': 'YR-MDI', 'instrument_capable': 'No'},
                {'actype': 5, 'registration': 'YR-MDH', 'instrument_capable': 'Yes'},
                {'actype': 5, 'registration': 'YR-YAN', 'instrument_capable': 'Yes'},
                {'actype': 5, 'registration': 'M-XHEC', 'instrument_capable': 'Yes'},
                {'actype': 7, 'registration': 'YR-MDA', 'instrument_capable': 'No'},
                {'actype': 7, 'registration': 'YR-MDN', 'instrument_capable': 'Yes'},
            ]

            company_data = [
                {'name': 'Şcoala Superioară de Aviaţie Civilă'},
                {'name': 'Raondom Air'},
                {'name': 'Imaginary Airlines'},
            ]

            with database.atomic():
                for data in pilot_data:
                    Pilot.create(**data)

                for data in airport_data:
                    Airport.create(**data)

                for data in actype_data:
                    ACType.create(**data)

                for data in aircraft_data:
                    Aircraft.create(**data)

                for data in company_data:
                    Company.create(**data)

        except peewee.OperationalError:
            print("Airport table already exists!")
 
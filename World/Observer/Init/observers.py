from World.Observer.WorldObserver import WorldObserver
from World.Observer.Constants import *


world_observer = WorldObserver(handlers_map={
    CHANGE_POSITION: [],
    WEATHER_SET_FINE: [],
    WEATHER_SET_RAIN: [],
    WEATHER_SET_SNOW: [],
    WEATHER_SET_STORM: [],
    WEATHER_SET_THUNDERS: [],
    WEATHER_SET_BLACK_RAIN: [],
})

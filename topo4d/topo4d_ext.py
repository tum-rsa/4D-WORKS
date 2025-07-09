from pystac.extensions.base import PropertiesExtension, ExtensionManagementMixin, SummariesExtension
from pystac import Item, STACError
from pystac.utils import StringEnum, get_required, map_opt
from pyproj import CRS
from pyproj.exceptions import CRSError
from typing import Literal


TOPO4D_SCHEMA_URI = "https://stac-extensions.github.io/topo4d/v1.0.0/schema.json"
PREFIX: str = "topo4d:"
DATATYPE_PROP = PREFIX + "data_type"  # required
CRS_PROP = PREFIX + "native_crs" # required
SENSOR_PROP = PREFIX + "sensor" # String
TS_PROP = PREFIX + "tz" # String
ACQUISITION_PROP = PREFIX + "acquisition_mode" # String
DURATION_PROP = PREFIX + "duration"  # Float
TRAJECTORY_PROP = PREFIX + "trajectory"  # Array
SCANPOS_PROP = PREFIX + "scan_position"  # Array
ORIENTATION_PROP = PREFIX + "orientation"  # String
POINTCOUNT_PROP = PREFIX + "point_count" # Integer
SPATIAL_RES_PROP = PREFIX + "spatial_resolution" # Float
MEASUREMENT_ERR_PROP = PREFIX + "measurement_error" # Float
TRAFO_GLOBAL_PROP = PREFIX + "global_trafo" # Array
TRAFO_META_PROP = PREFIX + "trafometa" # Object
PRODUCT_META_PROP = PREFIX + "productmeta" # Object


class CRSType:
    def __init__(self, value: str | None):
        if value is None or value.strip().lower() == "undefined":
            self.value = "Undefined"
        elif value.strip().lower() == "local":
            self.value = "Local"
        else:
            try:
                # Validate using pyproj
                _ = CRS.from_user_input(value)
                self.value = value
            except CRSError:
                raise ValueError(f"Invalid CRS string: {value}")
            
    def __str__(self):
        return self.value

    def __repr__(self):
        return f"CRSType({self.value!r})"
    
    def is_defined(self):
        return self.value not in {"Undefined", "Local"}

    def is_local(self):
        return self.value == "Local"

    def is_undefined(self):
        return self.value == "Undefined"
    
    def to_pyproj(self) -> CRS | None:
        if self.is_defined():
            return CRS.from_user_input(self.value)
        return None


class DataType(StringEnum):

    POINT_CLOUD = "point cloud"
    MESH = "mesh"
    RASTER = "raster"
    VECTOR = "vector"


class Topo4DExtension(PropertiesExtension, ExtensionManagementMixin):
    name: Literal["topo4d"] = "topo4d"

    def __init__(self, item: Item):
        self.item = item
        self.properties = item.properties

    def apply(
        self,
        data_type: DataType | str | None = None,
        native_crs: CRSType | str | None = None,
        sensor: str | None = None,
        tz: str | None = None,
        acquisition_mode: str | None = None,
        duration: float | None = None, 
        trajectory: list | None = None,
        scan_position: list | None = None,
        orientation: str | None = None,
        point_count: int | None = None,
        spatial_resolution: float | None = None,
        measurement_error: float | None = None,
        global_trafo: list | None = None,
        trafometa: dict | None = None,
        productmeta: dict | None = None

    ):
        """Applies the extension to the item."""
        if TOPO4D_SCHEMA_URI not in self.item.stac_extensions:
            self.item.stac_extensions.append(TOPO4D_SCHEMA_URI)

        self.data_type = data_type
        self.native_crs = native_crs
        self.sensor = sensor
        self.tz = tz
        self.acquisition_mode = acquisition_mode
        self.duration = duration
        self.trajectory = trajectory
        self.scan_position = scan_position
        self.orientation = orientation
        self.point_count = point_count
        self.spatial_resolution = spatial_resolution
        self.measurement_error = measurement_error
        self.global_trafo = global_trafo
        self.trafometa = trafometa
        self.productmeta = productmeta

    ######################################### Required Properties #########################################
    @property
    def native_crs(self) -> CRSType | None:
        return get_required(self._get_property(CRS_PROP, str), self, CRS_PROP)

    @native_crs.setter
    def native_crs(self, v: CRSType | str | None):
        if isinstance(v, CRSType):
            crs_str = str(v)
        elif isinstance(v, str) or v is None:
            crs_str = str(CRSType(v))
        else:
            raise TypeError(f"native_crs must be CRSType, str, or None — got {type(v)}")

        self._set_property(CRS_PROP, crs_str)

    @property
    def data_type(self) -> DataType:
        return get_required(self._get_property(DATATYPE_PROP, str), self, DATATYPE_PROP)
    
    @data_type.setter
    def data_type(self, v: DataType | str | None):
        if isinstance(v, DataType):
            self._set_property(DATATYPE_PROP, v.value)
        elif isinstance(v, str):
            self._set_property(DATATYPE_PROP, DataType(v).value)
        elif v is None:
            self._set_property(DATATYPE_PROP, None)
        else:
            raise TypeError(f"data_type must be DataType, str, or None — got {type(v)}")


    ########################################## Optional Properties #########################################
    @property
    def sensor(self) -> str:
        return self.properties.get(SENSOR_PROP)
    
    @sensor.setter
    def sensor(self, v: str | None):
        self._set_property(SENSOR_PROP, v, pop_if_none=True)

    @property
    def tz(self) -> str | None:
        return self.properties.get(TS_PROP)
    
    @tz.setter
    def tz(self, v: str | None):
        self._set_property(TS_PROP, v, pop_if_none=True)

    @property
    def acquisition_mode(self) -> str | None:
        return self.properties.get(ACQUISITION_PROP)
    
    @acquisition_mode.setter
    def acquisition_mode(self, v: str | None):
        self._set_property(ACQUISITION_PROP, v, pop_if_none=True)

    @property
    def duration(self) -> float | None:
        return self.properties.get(DURATION_PROP)
    
    @duration.setter
    def duration(self, v: float | None):
        self._set_property(DURATION_PROP, v, pop_if_none=True)


    @property
    def trajectory(self) -> list | None:
        return self.properties.get(TRAJECTORY_PROP)
    
    @trajectory.setter
    def trajectory(self, v: list | None):
        self._set_property(TRAJECTORY_PROP, v, pop_if_none=True)


    @property
    def scan_position(self) -> list | None:
        return self.properties.get(SCANPOS_PROP)
    
    @scan_position.setter
    def scan_position(self, v: list | None):
        self._set_property(SCANPOS_PROP, v, pop_if_none=True)


    @property
    def orientation(self) -> str | None:
        return self.properties.get(ORIENTATION_PROP)
    
    @orientation.setter
    def orientation(self, v: str | None):
        self._set_property(ORIENTATION_PROP, v, pop_if_none=True)


    @property
    def point_count(self) -> int | None:
        return self.properties.get(POINTCOUNT_PROP)
    
    @point_count.setter
    def point_count(self, v: int | None):
        self._set_property(POINTCOUNT_PROP, v, pop_if_none=True)


    @property
    def spatial_resolution(self) -> float | None:
        return self.properties.get(SPATIAL_RES_PROP)
    
    @spatial_resolution.setter
    def spatial_resolution(self, v: float | None):
        self._set_property(SPATIAL_RES_PROP, v, pop_if_none=True)


    @property
    def measurement_error(self) -> float | None:
        return self.properties.get(MEASUREMENT_ERR_PROP)
    
    @measurement_error.setter
    def measurement_error(self, v: float | None):
        self._set_property(MEASUREMENT_ERR_PROP, v, pop_if_none=True)

    @property
    def global_trafo(self) -> list | None:
        return self.properties.get(TRAFO_GLOBAL_PROP)
    
    @global_trafo.setter
    def global_trafo(self, v: list | None):
        self._set_property(TRAFO_GLOBAL_PROP, v, pop_if_none=True)


    @property
    def trafometa(self) -> dict | None:
        return self.properties.get(TRAFO_META_PROP)
    
    @trafometa.setter
    def trafometa(self, v: dict | None):
        self._set_property(TRAFO_META_PROP, v, pop_if_none=True)

    @property
    def productmeta(self) -> dict | None:
        return self.properties.get(PRODUCT_META_PROP)
    
    @productmeta.setter
    def productmeta(self, v: dict | None):
        self._set_property(PRODUCT_META_PROP, v, pop_if_none=True)
    
    @classmethod
    def get_schema_uri(cls) -> str:
        """Required method from PropertiesExtension abstract class"""
        return TOPO4D_SCHEMA_URI

    @classmethod
    def add_to(cls, item: Item) -> "Topo4DExtension":
        item.stac_extensions.append(TOPO4D_SCHEMA_URI)
        return cls(item)

    @classmethod
    def ext(cls, item: Item, add_if_missing: bool = False) -> "Topo4DExtension":
        if isinstance(item, Item):
            if add_if_missing and cls.get_schema_uri() not in item.stac_extensions:
                return cls.add_to(item)
            else:
                cls.ensure_has_extension(item, add_if_missing)
                return cls(item)
        else:
            raise pystac.ExtensionTypeError(
                f"Topo4DExtension does not apply to type '{type(item).__name__}'"
            )

********************
My first 3D scene
********************

Download the example: `material file <https://raw.githubusercontent.com/UmSenhorQualquer/py3dsceneeditor/refactoring/docs/_static/my-first-scene/teste.mtl>`_, `object file <https://raw.githubusercontent.com/UmSenhorQualquer/py3dsceneeditor/refactoring/docs/_static/my-first-scene/teste.obj>`_

.. code-block:: python

    from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
    from py3dengine.scenes.GLScene import GLScene
    from py3dengine.bin.RunScene import RunScene


    w = WavefrontOBJReader('DolphinScene.obj')

    scene = GLScene()
    scene.objects = w.objects
    scene.cameras = w.cameras

    camera = scene.getCamera('Camera1')

    ray     = camera.addRay( 100, 100 )
    collision = ray.collidePlanZ(0); 

    print('Point of collision with the Z plain', collision)

    floor   = scene.getObject('Floor')
    collision = ray.collide([floor])

    print('Point of collision with object Foor,', collision)

    run = RunScene(scene)
    run.startScene()



Stdout output

.. code-block:: bash

    Collision with the Z plain (-15.97673643616865, -18.90785099921925, 0.0)
    Collision with object Foor, (29.07119617403152, (-15.97673643616865, -18.90785099921925, 0.0), <py3dengine.objects.RectangleObject.RectangleObject object at 0x7f1198e7cac8>)


Output scene window

.. image:: /_static/example-result.png
   :scale: 100 %